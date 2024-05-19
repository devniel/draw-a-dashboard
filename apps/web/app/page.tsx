"use client";

import dynamic from "next/dynamic";
import { useState } from "react";
import { exportToBlob } from "@excalidraw/excalidraw";

// Since client components get prerenderd on server as well hence
// importing the excalidraw stuff dynamically with ssr false
const ExcalidrawWithClientOnly = dynamic(
  async () => (await import("../components/ExcalidrawWrapper")).default,
  {
    ssr: false,
  }
);

export default function Page() {
  const [excalidrawAPI, setExcalidrawAPI]: [any, any] = useState(null);

  const toDashboard = async () => {
    if (!excalidrawAPI) {
      return;
    }
    const elements = excalidrawAPI.getSceneElements();
    if (!elements || !elements.length) {
      return;
    }
    const blob = await exportToBlob({
      mimeType: "image/jpeg",
      quality: 1,
      elements,
      files: excalidrawAPI.getFiles(),
    });

    // Send the blob to the backend server directly
    const formData = new FormData();
    formData.append("image", blob, "canvas.jpg");

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/toDashboard`,
        {
          method: "POST",
          body: formData,
        }
      );

      if (response.ok) {
        const result = await response.json();
        console.log(result);
        window.open(process.env.NEXT_PUBLIC_RENDERER_URL, '_blank')?.focus();

      } else {
        console.error("Error uploading the image");
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div className="relative min-h-screen">
      <ExcalidrawWithClientOnly
        width="100%"
        height="100vh"
        excalidrawAPI={(api) => {
          console.log("api:", api);
          setExcalidrawAPI(api);
        }}
      />
      <button
        type="button"
        className="
        absolute 
        bottom-4 
        left-1/2 
        transform 
        -translate-x-1/2 
        z-50 
        inline-flex 
        items-center 
        rounded-md 
        bg-blue-900 
        px-6 
        py-3 
        text-lg 
        font-semibold 
        text-white 
        shadow-sm 
        hover:bg-indigo-500 
        focus-visible:outline 
        focus-visible:outline-2 
        focus-visible:outline-offset-2 
        focus-visible:outline-indigo-600
        cursor-pointer
      "
        onClick={toDashboard}
      >
        🪄 To Dashboard
      </button>
    </div>
  );
}
