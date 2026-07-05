export function formatSimpleMarkdown(text: string) {
  if (!text) return "";
  
  let formatted = text
    // Replace **bold** with <strong>bold</strong>
    .replace(/\*\*(.*?)\*\*/g, '<strong class="text-amber-300">$1</strong>')
    // Replace * bullet points with HTML bullet points and line breaks
    .replace(/(?:\s|^)\* (.*?)(?=(?:\s\* |$))/g, '<br/><span class="text-amber-500 mr-2">•</span> <span class="text-zinc-300">$1</span>')
    // Fallback for newlines
    .replace(/\n/g, '<br/>');
    
  return formatted;
}
