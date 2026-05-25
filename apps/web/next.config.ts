import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  transpilePackages: ["@sanson/types", "@sanson/shared", "@sanson/utils"],
};

export default nextConfig;
