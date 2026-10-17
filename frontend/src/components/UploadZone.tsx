import React from "react";
import { Upload, Loader2 } from "lucide-react";

interface UploadZoneProps {
  onUpload: (file: File) => void;
  state: string;
}

export function UploadZone({ onUpload, state }: UploadZoneProps) {
  return (
    <div className="flex flex-col items-center justify-center p-8 border-2 border-dashed border-slate-700 rounded-xl bg-slate-900/50 hover:bg-slate-800/50 transition-colors cursor-pointer relative">
      <input
        type="file"
        className="absolute inset-0 opacity-0 cursor-pointer"
        onChange={(e) => e.target.files?.[0] && onUpload(e.target.files[0])}
      />
      <Upload className="w-12 h-12 text-slate-500 mb-4" />
      <p className="text-slate-300 font-medium">Drop satellite imagery here</p>
      <p className="text-slate-500 text-sm">PNG, JPG up to 10MB</p>

      {state === "UPLOADING" && (
        <div className="absolute inset-0 bg-slate-900/80 flex items-center justify-center rounded-xl">
          <Loader2 className="w-8 h-8 text-blue-500 animate-spin" />
        </div>
      )}
    </div>
  );
}
