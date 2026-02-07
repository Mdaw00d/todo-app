'use client';

import React, { useState, useRef, useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { chatWithAssistant, ChatRequest, ChatResponse } from '@/services/api';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

const ChatComponent: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { user } = useAuth();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || !user || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputValue,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const requestBody: ChatRequest = {
        message: inputValue,
      };

      const data: ChatResponse = await chatWithAssistant(requestBody);

      const botMessage: Message = {
        id: Date.now().toString(),
        role: 'assistant',
        content: data.response,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      
      // Provide more specific error message based on the error type
      let errorMessageText = 'Sorry, I encountered an error processing your request. Please try again.';
      
      if (error instanceof Error) {
        if (error.message.includes('401') || error.message.toLowerCase().includes('unauthorized')) {
          errorMessageText = 'You are not authorized to use the chat. Please log in again.';
        } else if (error.message.includes('404')) {
          errorMessageText = 'The chat service is currently unavailable. Please try again later.';
        } else if (error.message.includes('Network Error') || error.message.includes('500')) {
          errorMessageText = 'The AI service is temporarily unavailable. Please try again later.';
        } else {
          errorMessageText = `Error: ${error.message}`;
        }
      }

      const errorMessage: Message = {
        id: Date.now().toString(),
        role: 'assistant',
        content: errorMessageText,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[500px] border border-gray-200 rounded-lg bg-white shadow-sm">
      <div className="p-4 border-b border-gray-200">
        <h2 className="text-lg font-semibold text-gray-800">AI Task Assistant</h2>
        <p className="text-sm text-gray-500">Chat with the AI to manage your tasks using natural language</p>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-center text-gray-500">
            <div className="mb-4 p-3 bg-indigo-100 rounded-full">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-indigo-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
            </div>
            <h3 className="text-lg font-medium text-gray-700 mb-1">Welcome to your AI Task Assistant!</h3>
            <p className="text-sm">Try saying things like:</p>
            <ul className="mt-2 text-xs text-left space-y-1">
              <li>• "Add a task to buy groceries"</li>
              <li>• "Show me my tasks"</li>
              <li>• "Mark the first task as complete"</li>
              <li>• "Delete my third task"</li>
            </ul>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] rounded-lg px-4 py-2 ${
                  message.role === 'user'
                    ? 'bg-indigo-600 text-white'
                    : 'bg-gray-200 text-gray-800'
                }`}
              >
                <div className="flex items-start space-x-2">
                  {message.role === 'assistant' && (
                    <div className="flex-shrink-0 pt-0.5">
                      <div className="w-6 h-6 rounded-full bg-indigo-500 flex items-center justify-center">
                        <span className="text-xs text-white font-bold">AI</span>
                      </div>
                    </div>
                  )}
                  <div>
                    <p className="text-sm">{message.content}</p>
                    <p className={`text-xs mt-1 ${message.role === 'user' ? 'text-indigo-200' : 'text-gray-500'}`}>
                      {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </p>
                  </div>
                  {message.role === 'user' && (
                    <div className="flex-shrink-0 pt-0.5">
                      <div className="w-6 h-6 rounded-full bg-gray-200 border border-gray-300 flex items-center justify-center">
                        <span className="text-xs text-gray-700 font-bold">U</span>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))
        )}
        {isLoading && (
          <div className="flex justify-start">
            <div className="max-w-[80%] rounded-lg px-4 py-2 bg-gray-200 text-gray-800">
              <div className="flex items-center space-x-2">
                <div className="flex-shrink-0 pt-0.5">
                  <div className="w-6 h-6 rounded-full bg-indigo-500 flex items-center justify-center">
                    <span className="text-xs text-white font-bold">AI</span>
                  </div>
                </div>
                <div className="flex space-x-1">
                  <div className="w-2 h-2 rounded-full bg-gray-500 animate-bounce"></div>
                  <div className="w-2 h-2 rounded-full bg-gray-500 animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  <div className="w-2 h-2 rounded-full bg-gray-500 animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                </div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSubmit} className="border-t border-gray-200 p-4 bg-white">
        <div className="flex space-x-2">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Type a message to your AI assistant..."
            className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
            disabled={isLoading || !user}
          />
          <button
            type="submit"
            className="bg-indigo-600 text-white rounded-lg px-4 py-2 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
            disabled={isLoading || !inputValue.trim() || !user}
          >
            Send
          </button>
        </div>
        <p className="text-xs text-gray-500 mt-2">
          Tip: You can say things like "Add a task to buy groceries" or "Show my tasks"
        </p>
      </form>
    </div>
  );
};

export default ChatComponent;