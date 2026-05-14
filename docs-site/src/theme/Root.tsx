import React, { type ReactNode, useEffect } from "react";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import { useLocation } from "@docusaurus/router";
import { NexlyProvider, useNexlyClient } from "@nexly/react-web";

type NexlyConfig = {
  appId?: string;
  ingestKey?: string;
};

let lastTrackedPath: string | null = null;

function getNexlyConfig(customFields: Record<string, unknown>): NexlyConfig {
  const nexly = customFields.nexly;

  if (!nexly || typeof nexly !== "object") {
    return {};
  }

  return nexly as NexlyConfig;
}

function NexlyPageviewTracker(): null {
  const location = useLocation();
  const client = useNexlyClient();

  useEffect(() => {
    if (!client) {
      return;
    }

    const path = `${location.pathname}${location.search}${location.hash}`;

    if (path === lastTrackedPath) {
      return;
    }

    lastTrackedPath = path;
    client.pageview(path);
  }, [client, location.hash, location.pathname, location.search]);

  return null;
}

export default function Root({ children }: { children: ReactNode }): ReactNode {
  const { siteConfig } = useDocusaurusContext();
  const { appId = "", ingestKey = "" } = getNexlyConfig(siteConfig.customFields);

  if (!appId.trim() || !ingestKey.trim()) {
    return children;
  }

  return (
    <NexlyProvider appId={appId} ingestKey={ingestKey} autoEngagement>
      <NexlyPageviewTracker />
      {children}
    </NexlyProvider>
  );
}
