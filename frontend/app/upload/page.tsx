import { ProtectedShell } from "@/components/layout/protected-shell";
import { UploadDropzone } from "@/components/upload/upload-dropzone";

export default function UploadPage() {
  return (
    <ProtectedShell>
      <UploadDropzone />
    </ProtectedShell>
  );
}
