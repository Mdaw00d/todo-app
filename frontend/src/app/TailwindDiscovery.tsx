// Dummy component to help Tailwind discover classes used with @apply
// This component won't be rendered but helps Turbopack's Tailwind plugin discover the classes

export default function TailwindDiscovery() {
  return (
    <div className="hidden">
      {/* Button classes */}
      <div className="px-4 py-2.5 rounded-lg font-medium transition-all duration-200 flex items-center justify-center gap-2" />
      <div className="bg-indigo-600 text-white" />
      <div className="hover:bg-indigo-700 active:bg-indigo-800" />
      <div className="shadow-lg shadow-indigo-500/30 hover:shadow-indigo-500/40" />
      <div className="bg-white text-gray-700 border border-gray-200" />
      <div className="hover:bg-gray-50 hover:border-gray-300" />
      <div className="bg-red-500 text-white" />
      <div className="hover:bg-red-600 active:bg-red-700" />
      <div className="bg-transparent text-gray-600" />
      <div className="hover:bg-gray-100 hover:text-gray-900" />
      <div className="px-3 py-1.5 text-sm" />
      <div className="px-6 py-3 text-lg" />

      {/* Input field classes */}
      <div className="w-full px-4 py-3 bg-white border border-gray-200 rounded-lg text-gray-900 placeholder-gray-400 transition-all duration-200" />
      <div className="focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent" />
      <div className="hover:border-gray-300" />
      <div className="bg-gray-50 cursor-not-allowed" />

      {/* Card classes */}
      <div className="bg-white rounded-2xl shadow-xl p-6" />
      <div className="transition-all duration-200 hover:shadow-2xl hover:-translate-y-1" />

      {/* Message classes */}
      <div className="text-red-600 text-sm bg-red-50 border border-red-100 rounded-lg p-3 flex items-center gap-2" />
      <div className="text-green-600 text-sm bg-green-50 border border-green-100 rounded-lg p-3 flex items-center gap-2" />

      {/* Checkbox classes */}
      <div className="w-6 h-6 rounded-full border-2 flex items-center justify-center transition-all duration-200 cursor-pointer" />
      <div className="border-gray-300 hover:border-indigo-500 hover:bg-indigo-50" />
      <div className="bg-green-500 border-green-500 text-white" />

      {/* Task item classes */}
      <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100 transition-all duration-200" />
      <div className="hover:shadow-md hover:border-gray-200" />
      <div className="bg-gray-50 opacity-75" />

      {/* Animation classes - these are essential for Tailwind to discover custom animations */}
      <div className="animate-fadeIn" />
      <div className="animate-slideIn" />
    </div>
  );
}