"use client";

import { useState, useRef, useEffect } from "react";
import { Send, Bot, User } from "lucide-react";
import { DashboardShell } from "@/components/layout/dashboard-shell";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
}

export default function ClientChatPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "welcome",
      role: "assistant",
      content:
        "Welcome to SANSON Law Firm. I'm your AI Legal Intake Assistant — your free first consultation layer. Please describe your legal concern, and I'll help gather and organize the details for our legal team. I cannot provide legal advice, but I can help structure your case.",
    },
  ]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  const sendMessage = async () => {
    if (!input.trim() || isTyping) return;

    const userMsg: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input.trim(),
    };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setIsTyping(true);

    // Phase 2: connect to streaming API
    setTimeout(() => {
      const assistantMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content:
          "Thank you for sharing that. To help organize your case, could you tell me: (1) When did this issue begin? (2) Are there any documents or evidence you have? (3) What outcome are you hoping for? Once I have enough information, I can summarize your case and let you know if proceeding with formal legal services makes sense.",
      };
      setMessages((prev) => [...prev, assistantMsg]);
      setIsTyping(false);
    }, 1500);
  };

  return (
    <DashboardShell
      role="client"
      title="AI Legal Chat"
      subtitle="Free AI consultation — not a booking"
    >
      <div className="flex h-[calc(100vh-12rem)] flex-col glass-card overflow-hidden">
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={cn(
                "flex gap-3 animate-fade-in",
                msg.role === "user" ? "flex-row-reverse" : ""
              )}
            >
              <div
                className={cn(
                  "flex h-8 w-8 shrink-0 items-center justify-center rounded-full",
                  msg.role === "assistant"
                    ? "bg-gradient-to-br from-pink-600 to-pink-400"
                    : "bg-white/10"
                )}
              >
                {msg.role === "assistant" ? (
                  <Bot className="h-4 w-4 text-white" />
                ) : (
                  <User className="h-4 w-4" />
                )}
              </div>
              <div
                className={cn(
                  "max-w-[75%] rounded-2xl px-4 py-3 text-sm",
                  msg.role === "assistant"
                    ? "bg-white/5 border border-pink-500/10"
                    : "bg-pink-600/20 border border-pink-500/20"
                )}
              >
                {msg.content}
              </div>
            </div>
          ))}
          {isTyping && (
            <div className="flex gap-3">
              <div className="flex h-8 w-8 items-center justify-center rounded-full bg-gradient-to-br from-pink-600 to-pink-400">
                <Bot className="h-4 w-4 text-white" />
              </div>
              <div className="flex items-center gap-1 rounded-2xl bg-white/5 px-4 py-3">
                <span className="typing-dot h-2 w-2 rounded-full bg-pink-400" />
                <span className="typing-dot h-2 w-2 rounded-full bg-pink-400" />
                <span className="typing-dot h-2 w-2 rounded-full bg-pink-400" />
              </div>
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        <div className="border-t border-pink-500/10 p-4">
          <div className="flex gap-3">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && sendMessage()}
              placeholder="Describe your legal concern..."
              className="flex-1 rounded-xl border border-pink-500/20 bg-white/5 px-4 py-3 text-sm focus:border-pink-500/50 focus:outline-none"
            />
            <Button onClick={sendMessage} disabled={!input.trim() || isTyping}>
              <Send className="h-4 w-4" />
            </Button>
          </div>
          <p className="mt-2 text-center text-xs text-[var(--muted)]">
            AI intake only — not legal advice. Proceed with legal action when ready.
          </p>
        </div>
      </div>
    </DashboardShell>
  );
}
