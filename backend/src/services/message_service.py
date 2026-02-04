"""
Message service for the Todo AI Chatbot.
Contains business logic for message operations.
"""

from typing import List, Optional
from sqlmodel import select, and_
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from ..models.message import Message, MessageCreate, MessageUpdate, MessageRead
from ..exceptions.handlers import ConversationNotFoundException, UnauthorizedAccessException, InvalidTaskOperationError


class MessageService:
    """Service class for managing message operations."""

    @staticmethod
    async def create_message(session: AsyncSession, message_create: MessageCreate) -> MessageRead:
        """
        Create a new message.

        Args:
            session: Database session
            message_create: Message creation data

        Returns:
            MessageRead: Created message
        """
        try:
            # Validate user_id format
            if not message_create.user_id or len(message_create.user_id.strip()) == 0:
                raise InvalidTaskOperationError("User ID cannot be empty")

            # Validate content
            if not message_create.content or len(message_create.content.strip()) == 0:
                raise InvalidTaskOperationError("Message content cannot be empty")

            # Create message instance
            db_message = Message.model_validate(message_create)

            # Add to session and commit
            session.add(db_message)
            await session.commit()
            await session.refresh(db_message)

            # Return as MessageRead
            return MessageRead.model_validate(db_message)

        except SQLAlchemyError as e:
            await session.rollback()
            raise InvalidTaskOperationError(f"Database error while creating message: {str(e)}")

    @staticmethod
    async def get_message_by_id(session: AsyncSession, message_id: int, user_id: str) -> MessageRead:
        """
        Get a message by its ID for a specific user.

        Args:
            session: Database session
            message_id: ID of the message to retrieve
            user_id: ID of the user who owns the message

        Returns:
            MessageRead: Retrieved message
        """
        try:
            # Query for the message with the given ID and user ID
            statement = select(Message).where(and_(Message.id == message_id, Message.user_id == user_id))
            result = await session.execute(statement)
            message = result.first()

            if not message:
                raise InvalidTaskOperationError(f"Message with ID {message_id} not found for user {user_id}")

            return MessageRead.model_validate(message)

        except SQLAlchemyError as e:
            raise InvalidTaskOperationError(f"Database error while retrieving message: {str(e)}")

    @staticmethod
    async def get_messages_by_conversation(
        session: AsyncSession,
        conversation_id: int,
        user_id: str
    ) -> List[MessageRead]:
        """
        Get all messages for a specific conversation.

        Args:
            session: Database session
            conversation_id: ID of the conversation whose messages to retrieve
            user_id: ID of the user who owns the conversation

        Returns:
            List[MessageRead]: List of conversation's messages
        """
        try:
            # Build query for messages belonging to the conversation
            query = select(Message).where(
                and_(
                    Message.conversation_id == conversation_id,
                    Message.user_id == user_id
                )
            ).order_by(Message.created_at.asc())

            result = await session.execute(query)
            messages = result.all()

            # Convert to MessageRead objects
            return [MessageRead.model_validate(msg) for msg in messages]

        except SQLAlchemyError as e:
            raise InvalidTaskOperationError(f"Database error while retrieving messages: {str(e)}")

    @staticmethod
    async def get_recent_messages_by_user(
        session: AsyncSession,
        user_id: str,
        limit: int = 50
    ) -> List[MessageRead]:
        """
        Get recent messages for a specific user.

        Args:
            session: Database session
            user_id: ID of the user whose messages to retrieve
            limit: Maximum number of messages to return

        Returns:
            List[MessageRead]: List of user's recent messages
        """
        try:
            # Build query for messages belonging to the user
            query = select(Message).where(Message.user_id == user_id).order_by(
                Message.created_at.desc()
            ).limit(limit)

            result = await session.execute(query)
            messages = result.all()

            # Convert to MessageRead objects and sort chronologically
            message_list = [MessageRead.model_validate(msg) for msg in messages]
            message_list.sort(key=lambda x: x.created_at)

            return message_list

        except SQLAlchemyError as e:
            raise InvalidTaskOperationError(f"Database error while retrieving messages: {str(e)}")

    @staticmethod
    async def update_message(
        session: AsyncSession,
        message_id: int,
        user_id: str,
        message_update: MessageUpdate
    ) -> MessageRead:
        """
        Update a message (though messages are typically immutable).

        Args:
            session: Database session
            message_id: ID of the message to update
            user_id: ID of the user who owns the message
            message_update: Message update data

        Returns:
            MessageRead: Updated message
        """
        try:
            # First, get the existing message to verify it exists and belongs to the user
            statement = select(Message).where(and_(Message.id == message_id, Message.user_id == user_id))
            result = await session.execute(statement)
            existing_message = result.first()

            if not existing_message:
                raise InvalidTaskOperationError(f"Message with ID {message_id} not found for user {user_id}")

            # For this application, we don't allow updating messages since they're immutable
            raise InvalidTaskOperationError("Messages cannot be updated as they are immutable")

        except SQLAlchemyError as e:
            await session.rollback()
            raise InvalidTaskOperationError(f"Database error while updating message: {str(e)}")

    @staticmethod
    async def delete_message(session: AsyncSession, message_id: int, user_id: str) -> bool:
        """
        Delete a message.

        Args:
            session: Database session
            message_id: ID of the message to delete
            user_id: ID of the user who owns the message

        Returns:
            bool: True if message was deleted
        """
        try:
            # First, get the existing message to verify it exists and belongs to the user
            statement = select(Message).where(and_(Message.id == message_id, Message.user_id == user_id))
            result = await session.execute(statement)
            existing_message = result.first()

            if not existing_message:
                raise InvalidTaskOperationError(f"Message with ID {message_id} not found for user {user_id}")

            # Delete the message
            await session.delete(existing_message)
            await session.commit()

            return True

        except SQLAlchemyError as e:
            await session.rollback()
            raise InvalidTaskOperationError(f"Database error while deleting message: {str(e)}")