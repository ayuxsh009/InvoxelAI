import { ChatPanel } from "@/components/chat/chat-panel";
import { ProtectedShell } from "@/components/layout/protected-shell";

export default function ChatPage() {
  return (
    <ProtectedShell>
      <ChatPanel />
    </ProtectedShell>
  );
}
