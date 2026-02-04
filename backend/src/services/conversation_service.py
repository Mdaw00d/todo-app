"""
Conversation service for the Todo AI Chatbot.
Contains business logic for conversation operations.
"""

from typing import List, Optional, Dict, Any
from sqlmodel import select, and_
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from ..models.conversation import Conversation, ConversationCreate, ConversationUpdate, ConversationRead
from ..exceptions.handlers import ConversationNotFoundException, UnauthorizedAccessException, InvalidTaskOperationError


class ConversationService:
    """Service class for managing conversation operations."""

    @staticmethod
    async def create_conversation(session: AsyncSession, conversation_create: ConversationCreate) -> ConversationRead:
        """
        Create a new conversation.

        Args:
            session: Database session
            conversation_create: Conversation creation data

        Returns:
            ConversationRead: Created conversation
        """
        try:
            # Validate user_id format
            if not conversation_create.user_id or len(conversation_create.user_id.strip()) == 0:
                raise InvalidTaskOperationError("User ID cannot be empty")

            # Create conversation instance with empty context
            db_conversation = Conversation.model_validate(conversation_create)
            db_conversation.set_context({})  # Initialize with empty context

            # Add to session and commit
            session.add(db_conversation)
            await session.commit()
            await session.refresh(db_conversation)

            # Return as ConversationRead
            return ConversationRead.model_validate(db_conversation)

        except SQLAlchemyError as e:
            await session.rollback()
            raise InvalidTaskOperationError(f"Database error while creating conversation: {str(e)}")

    @staticmethod
    async def get_conversation_by_id(session: AsyncSession, conversation_id: int, user_id: str) -> ConversationRead:
        """
        Get a conversation by its ID for a specific user.

        Args:
            session: Database session
            conversation_id: ID of the conversation to retrieve
            user_id: ID of the user who owns the conversation

        Returns:
            ConversationRead: Retrieved conversation
        """
        try:
            # Query for the conversation with the given ID and user ID
            statement = select(Conversation).where(
                and_(Conversation.id == conversation_id, Conversation.user_id == user_id)
            )
            result = await session.execute(statement)
            conversation = result.first()

            if not conversation:
                raise ConversationNotFoundException(conversation_id)

            return ConversationRead.model_validate(conversation)

        except SQLAlchemyError as e:
            raise InvalidTaskOperationError(f"Database error while retrieving conversation: {str(e)}")

    @staticmethod
    async def get_conversations_by_user(session: AsyncSession, user_id: str) -> List[ConversationRead]:
        """
        Get all conversations for a specific user.

        Args:
            session: Database session
            user_id: ID of the user whose conversations to retrieve

        Returns:
            List[ConversationRead]: List of user's conversations
        """
        try:
            # Build query for conversations belonging to the user
            query = select(Conversation).where(Conversation.user_id == user_id)
            result = await session.execute(query)
            conversations = result.all()

            # Convert to ConversationRead objects
            return [ConversationRead.model_validate(conv) for conv in conversations]

        except SQLAlchemyError as e:
            raise InvalidTaskOperationError(f"Database error while retrieving conversations: {str(e)}")

    @staticmethod
    async def update_conversation(
        session: AsyncSession,
        conversation_id: int,
        user_id: str,
        conversation_update: ConversationUpdate
    ) -> ConversationRead:
        """
        Update a conversation.

        Args:
            session: Database session
            conversation_id: ID of the conversation to update
            user_id: ID of the user who owns the conversation
            conversation_update: Conversation update data

        Returns:
            ConversationRead: Updated conversation
        """
        try:
            # First, get the existing conversation to verify it exists and belongs to the user
            statement = select(Conversation).where(
                and_(Conversation.id == conversation_id, Conversation.user_id == user_id)
            )
            result = await session.execute(statement)
            existing_conversation = result.first()

            if not existing_conversation:
                raise ConversationNotFoundException(conversation_id)

            # Update conversation with new values
            update_data = conversation_update.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(existing_conversation, field, value)

            # Update timestamp
            existing_conversation.updated_at = existing_conversation.__class__.updated_at.default.factory()

            # Commit changes
            await session.commit()
            await session.refresh(existing_conversation)

            return ConversationRead.model_validate(existing_conversation)

        except SQLAlchemyError as e:
            await session.rollback()
            raise InvalidTaskOperationError(f"Database error while updating conversation: {str(e)}")

    @staticmethod
    async def delete_conversation(session: AsyncSession, conversation_id: int, user_id: str) -> bool:
        """
        Delete a conversation.

        Args:
            session: Database session
            conversation_id: ID of the conversation to delete
            user_id: ID of the user who owns the conversation

        Returns:
            bool: True if conversation was deleted
        """
        try:
            # First, get the existing conversation to verify it exists and belongs to the user
            statement = select(Conversation).where(
                and_(Conversation.id == conversation_id, Conversation.user_id == user_id)
            )
            result = await session.execute(statement)
            existing_conversation = result.first()

            if not existing_conversation:
                raise ConversationNotFoundException(conversation_id)

            # Delete the conversation
            await session.delete(existing_conversation)
            await session.commit()

            return True

        except SQLAlchemyError as e:
            await session.rollback()
            raise InvalidTaskOperationError(f"Database error while deleting conversation: {str(e)}")

    @staticmethod
    async def update_conversation_context(
        session: AsyncSession,
        conversation_id: int,
        user_id: str,
        context_updates: Dict[str, Any]
    ) -> ConversationRead:
        """
        Update the context of a conversation.

        Args:
            session: Database session
            conversation_id: ID of the conversation to update
            user_id: ID of the user who owns the conversation
            context_updates: Dictionary of context updates

        Returns:
            ConversationRead: Updated conversation
        """
        try:
            # First, get the existing conversation to verify it exists and belongs to the user
            statement = select(Conversation).where(
                and_(Conversation.id == conversation_id, Conversation.user_id == user_id)
            )
            result = await session.execute(statement)
            existing_conversation = result.first()

            if not existing_conversation:
                raise ConversationNotFoundException(conversation_id)

            # Get current context and update with new values
            current_context = existing_conversation.get_context()
            current_context.update(context_updates)

            # Set the updated context
            existing_conversation.set_context(current_context)

            # Update timestamp
            existing_conversation.updated_at = existing_conversation.__class__.updated_at.default.factory()

            # Commit changes
            await session.commit()
            await session.refresh(existing_conversation)

            return ConversationRead.model_validate(existing_conversation)

        except SQLAlchemyError as e:
            await session.rollback()
            raise InvalidTaskOperationError(f"Database error while updating conversation context: {str(e)}")

    @staticmethod
    async def get_conversation_context(
        session: AsyncSession,
        conversation_id: int,
        user_id: str
    ) -> Dict[str, Any]:
        """
        Get the context of a conversation.

        Args:
            session: Database session
            conversation_id: ID of the conversation to retrieve
            user_id: ID of the user who owns the conversation

        Returns:
            Dict: Conversation context
        """
        try:
            # Get the conversation
            conversation = await ConversationService.get_conversation_by_id(
                session, conversation_id, user_id
            )

            # Parse and return the context
            if conversation.context_data:
                import json
                try:
                    return json.loads(conversation.context_data)
                except json.JSONDecodeError:
                    return {}

            return {}

        except Exception as e:
            raise InvalidTaskOperationError(f"Error retrieving conversation context: {str(e)}")