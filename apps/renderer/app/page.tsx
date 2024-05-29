"use client";
import Button from '@mui/material/Button';

export default function Page() {
  return (
    <>
      <Button
        variant="outlined"
        style={{ position: 'absolute', left: 50, top: 20, width: 180, height: 80 }}
      >
        CLICK
      </Button>

      <FloatingButton />

      <Button
        variant="outlined"
        style={{ position: 'absolute', left: 300, top: 200, width: 180, height: 80 }}
      >
        ENTER
      </Button>
    </>
  );
}

const FloatingButton = () => (
  <Button 
    variant="outlined"
    style={{ 
      position: 'absolute', 
      left: 20, 
      top: 120, 
      width: 240, 
      height: 120 
    }}
  >
    CLICK
  </Button>
);