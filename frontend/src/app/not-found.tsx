import Link from "next/link";
import { Button } from "@/components/ui/button";

export default function NotFound() {
  return (
    <div className="container px-4 py-16 flex flex-col items-center justify-center text-center min-h-[60vh]">
      <h2 className="text-3xl font-bold tracking-tight">404 - Not Found</h2>
      <p className="mt-4 text-muted-foreground">The page you are looking for does not exist in this workspace.</p>
      <div className="mt-8">
        <Link href="/">
          <Button>Return Home</Button>
        </Link>
      </div>
    </div>
  );
}
