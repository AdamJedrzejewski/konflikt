"use client";

import { useEffect, useState } from "react";
import { getMe, type Me } from "@/lib/api";

const ROLE_LABELS: Record<Me["role"], string> = {
  operator: "operator",
  tester: "tester",
};

/** Kto korzysta z aplikacji i w jakiej roli. */
export function UserBadge() {
  const [me, setMe] = useState<Me | null>(null);

  useEffect(() => {
    getMe().then(setMe).catch(() => setMe(null));
  }, []);

  if (!me) return null;
  return (
    <span className="text-xs text-ink-muted" title="Zalogowany użytkownik">
      {me.email} · {ROLE_LABELS[me.role]}
    </span>
  );
}
