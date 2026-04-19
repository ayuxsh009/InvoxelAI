"use client";

import { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";
import { Loader2, UploadCloud } from "lucide-react";
import { toast } from "sonner";

import { invoiceApi } from "@/lib/api";

export function UploadDropzone() {
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (!acceptedFiles.length) return;
    setUploading(true);
    setProgress(0);
    try {
      const file = acceptedFiles[0];
      await invoiceApi.upload(file, setProgress);
      toast.success("Invoice processed successfully");
    } catch {
      toast.error("Upload failed. Check file format and token.");
    } finally {
      setUploading(false);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "application/pdf": [".pdf"],
      "image/jpeg": [".jpg", ".jpeg"],
      "image/png": [".png"]
    },
    maxFiles: 1
  });

  return (
    <div
      {...getRootProps()}
      className="cursor-pointer rounded-2xl border-2 border-dashed border-border bg-card p-10 text-center transition hover:border-primary"
    >
      <input {...getInputProps()} />
      <div className="mx-auto flex max-w-md flex-col items-center gap-3">
        {uploading ? <Loader2 className="h-10 w-10 animate-spin" /> : <UploadCloud className="h-10 w-10" />}
        <h3 className="text-xl font-bold">{isDragActive ? "Drop invoice here" : "Drag and drop invoice"}</h3>
        <p className="text-sm text-muted-foreground">PDF, JPG, PNG. OCR supports English + Hindi.</p>
        {uploading ? <p className="text-sm font-semibold">Uploading: {progress}%</p> : null}
      </div>
    </div>
  );
}
