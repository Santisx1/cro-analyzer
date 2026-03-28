import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'CRO Analyzer - Conversion Rate Optimization',
  description: 'Automated CRO analysis and optimization recommendations',
  icons: {
    icon: '/favicon.ico',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pt-BR">
      <body>{children}</body>
    </html>
  );
}
