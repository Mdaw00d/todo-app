"""
MCP tools for conversation operations in the Todo AI Chatbot.
These tools allow the AI agent to perform conversation operations through MCP.
"""

from typing import Optional, List, Dict, Any
from sqlmodel.ext.asyncio.session import AsyncSession
from ..services.conversation_service import ConversationService
from ..services.message_service import MessageService
from ..models.conversation import ConversationCreate
from ..models.message import MessageCreate, MessageRole
from ..database import get_async_session
from ..utils.validation import validate_user_id, validate_message_content


class ConversationMCPTools:
    """Class containing MCP tools for conversation operations."""

    @staticmethod
    async def create_conversation(
        user_id: str
    ) -> dict:
        """
        Create a new conversation for a user.

        Args:
            user_id: ID of the user creating the conversation

        Returns:
            dict: Result of the operation
        """
        # Validate inputs
        if not validate_user_id(user_id):
            return {"success": False, "error": "Invalid user ID format"}

        try:
            # Create a new database session
            async with get_async_session() as session:
                # Prepare the conversation creation data
                conversation_create = ConversationCreate(
                    user_id=user_id
                )

                # Call the service to create the conversation
                created_conversation = await ConversationService.create_conversation(
                    session, conversation_create
                )

                return {
                    "success": True,
                    "conversation_id": created_conversation.id,
                    "message": f"Conversation created successfully"
                }

        except Exception as e:
            return {"success": False, "error": f"Failed to create conversation: {str(e)}"}

    @staticmethod
    async def add_message_to_conversation(
        user_id: str,
        conversation_id: int,
        role: str,
        content: str
    ) -> dict:
        """
        Add a message to a conversation.

        Args:
            user_id: ID of the user adding the message
            conversation_id: ID of the conversation to add to
            role: Role of the message ('user' or 'assistant')
            content: Content of the message

        Returns:
            dict: Result of the operation
        """
        # Validate inputs
        if not validate_user_id(user_id):
            return {"success": False, "error": "Invalid user ID format"}

        if not isinstance(conversation_id, int) or conversation_id <= 0:
            return {"success": False, "error": "Invalid conversation ID"}

        if role not in ["user", "assistant"]:
            return {"success": False, "error": "Invalid role. Use 'user' or 'assistant'"}

        is_valid, error_msg = validate_message_content(content)
        if not is_valid:
            return {"success": False, "error": error_msg}

        try:
            # Create a new database session
            async with get_async_session() as session:
                # Prepare the message creation data
                message_create = MessageCreate(
                    user_id=user_id,
                    conversation_id=conversation_id,
                    role=MessageRole(role),
                    content=content
                )

                # Call the service to create the message
                created_message = await MessageService.create_message(session, message_create)

                return {
                    "success": True,
                    "message_id": created_message.id,
                    "message": f"Message added to conversation successfully"
                }

        except Exception as e:
            return {"success": False, "error": f"Failed to add message to conversation: {str(e)}"}

    @staticmethod
    async def get_conversation_history(
        user_id: str,
        conversation_id: int
    ) -> dict:
        """
        Get the message history of a conversation.

        Args:
            user_id: ID of the user requesting the history
            conversation_id: ID of the conversation to retrieve

        Returns:
            dict: Result of the operation with message history
        """
        # Validate inputs
        if not validate_user_id(user_id):
            return {"success": False, "error": "Invalid user ID format"}

        if not isinstance(conversation_id, int) or conversation_id <= 0:
            return {"success": False, "error": "Invalid conversation ID"}

        try:
            # Create a new database session
            async with get_async_session() as session:
                # Call the service to get messages for the conversation
                messages = await MessageService.get_messages_by_conversation(
                    session, conversation_id, user_id
                )

                # Format the result
                message_list = []
                for message in messages:
                    message_dict = {
                        "id": message.id,
                        "role": message.role.value,
                        "content": message.content,
                        "created_at": message.created_at.isoformat() if message.created_at else None
                    }
                    message_list.append(message_dict)

                return {
                    "success": True,
                    "messages": message_list,
                    "count": len(message_list)
                }

        except Exception as e:
            return {"success": False, "error": f"Failed to retrieve conversation history: {str(e)}"}

    @staticmethod
    async def get_user_conversations(
        user_id: str
    ) -> dict:
        """
        Get all conversations for a user.

        Args:
            user_id: ID of the user whose conversations to retrieve

        Returns:
            dict: Result of the operation with conversation list
        """
        # Validate inputs
        if not validate_user_id(user_id):
            return {"success": False, "error": "Invalid user ID format"}

        try:
            # Create a new database session
            async with get_async_session() as session:
                # Call the service to get conversations for the user
                conversations = await ConversationService.get_conversations_by_user(
                    session, user_id
                )

                # Format the result
                conversation_list = []
                for conversation in conversations:
                    conversation_dict = {
                        "id": conversation.id,
                        "created_at": conversation.created_at.isoformat() if conversation.created_at else None,
                        "updated_at": conversation.updated_at.isoformat() if conversation.updated_at else None
                    }
                    conversation_list.append(conversation_dict)

                return {
                    "success": True,
                    "conversations": conversation_list,
                    "count": len(conversation_list)
                }

        except Exception as e:
            return {"success": False, "error": f"Failed to retrieve user conversations: {str(e)}"}

    @staticmethod
    async def update_conversation_context(
        user_id: str,
        conversation_id: int,
        context_updates: Dict[str, Any]
    ) -> dict:
        """
        Update the context of a conversation.

        Args:
            user_id: ID of the user who owns the conversation
            conversation_id: ID of the conversation to update
            context_updates: Dictionary of context updates to apply

        Returns:
            dict: Result of the operation
        """
        # Validate inputs
        if not validate_user_id(user_id):
            return {"success": False, "error": "Invalid user ID format"}

        if not isinstance(conversation_id, int) or conversation_id <= 0:
            return {"success": False, "error": "Invalid conversation ID"}

        try:
            # Create a new database session
            async with get_async_session() as session:
                # Call the service to update the conversation context
                updated_conversation = await ConversationService.update_conversation_context(
                    session, conversation_id, user_id, context_updates
                )

                return {
                    "success": True,
                    "conversation_id": updated_conversation.id,
                    "message": "Conversation context updated successfully"
                }

        except Exception as e:
            return {"success": False, "error": f"Failed to update conversation context: {str(e)}"}

    @staticmethod
    async def get_conversation_context(
        user_id: str,
        conversation_id: int
    ) -> dict:
        """
        Get the context of a conversation.

        Args:
            user_id: ID of the user who owns the conversation
            conversation_id: ID of the conversation to retrieve

        Returns:
            dict: Result of the operation with conversation context
        """
        # Validate inputs
        if not validate_user_id(user_id):
            return {"success": False, "error": "Invalid user ID format"}

        if not isinstance(conversation_id, int) or conversation_id <= 0:
            return {"success": False, "error": "Invalid conversation ID"}

        try:
            # Create a new database session
            async with get_async_session() as session:
                # Call the service to get the conversation context
                context = await ConversationService.get_conversation_context(
                    session, conversation_id, user_id
                )

                return {
                    "success": True,
                    "context": context
                }

        except Exception as e:
            return {"success": False, "error": f"Failed to retrieve conversation context: {str(e)}"}