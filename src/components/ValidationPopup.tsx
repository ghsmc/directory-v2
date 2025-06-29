import { motion } from 'framer-motion';
import { Loader2, MailCheck, RefreshCw, Edit2 } from 'lucide-react';

interface ValidationPopupProps {
  message: string;
  show: boolean;
  onClose: () => void;
  email?: string;
  showOpenEmailButton?: boolean;
  showSpinner?: boolean;
  isPersistent?: boolean;
  onResend?: () => void;
  onChangeEmail?: () => void;
  resendDisabled?: boolean;
  resendCooldown?: number;
}

function getEmailProviderUrl(email?: string): string | null {
  if (!email) return null;
  const domain = email.split('@')[1]?.toLowerCase();
  if (!domain) return null;
  if (domain.includes('gmail')) return 'https://mail.google.com';
  if (domain.includes('yahoo')) return 'https://mail.yahoo.com';
  if (domain.includes('outlook') || domain.includes('hotmail') || domain.includes('live')) return 'https://outlook.live.com';
  if (domain.includes('edu')) return `https://mail.${domain}`;
  return `https://${domain}`;
}

export function ValidationPopup({
  message,
  show,
  onClose,
  email,
  showOpenEmailButton,
  showSpinner,
  isPersistent,
  onResend,
  onChangeEmail,
  resendDisabled,
  resendCooldown
}: ValidationPopupProps) {
  if (!show) return null;
  const providerUrl = getEmailProviderUrl(email);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/30">
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: 10 }}
        className="bg-white rounded-xl shadow-2xl border border-gray-200 px-6 py-6 flex flex-col items-center gap-3 max-w-xs w-full"
      >
        <img
          src="/logo.png"
          alt="Milo"
          className="w-8 h-8 rounded object-contain mb-1"
        />
        <span className="text-base text-gray-800 text-center font-medium">{message}</span>
        {email && (
          <div className="flex items-center gap-2 text-sm text-gray-600 bg-gray-100 rounded px-3 py-1 mt-1">
            <MailCheck size={16} className="text-blue-500" />
            <span>{email}</span>
          </div>
        )}
        {showSpinner && (
          <div className="flex flex-col items-center mt-2">
            <Loader2 className="animate-spin text-blue-500 mb-1" size={28} />
            <span className="text-xs text-gray-500">Waiting for verification...</span>
          </div>
        )}
        <div className="flex flex-col gap-2 w-full mt-2">
          {showOpenEmailButton && providerUrl && (
            <a
              href={providerUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="bg-blue-600 text-white px-4 py-2 rounded-lg font-semibold shadow hover:bg-blue-700 transition-colors text-center"
            >
              {(() => {
                if (!email) return 'Open Mail';
                const domain = email.split('@')[1];
                if (!domain) return 'Open Mail';
                const provider = domain.split('.')[0];
                return `Open ${provider.charAt(0).toUpperCase() + provider.slice(1)} Mail`;
              })()}
            </a>
          )}
          {onResend && (
            <button
              onClick={onResend}
              disabled={resendDisabled}
              className={`flex items-center justify-center gap-2 bg-gray-200 text-gray-700 px-4 py-2 rounded-lg font-medium transition-colors hover:bg-gray-300 disabled:opacity-60 disabled:cursor-not-allowed`}
            >
              <RefreshCw size={16} />
              {resendDisabled && resendCooldown ? `Resend in ${resendCooldown}s` : 'Resend Email'}
            </button>
          )}
          {onChangeEmail && (
            <button
              onClick={onChangeEmail}
              className="flex items-center justify-center gap-2 bg-gray-100 text-blue-600 px-4 py-2 rounded-lg font-medium transition-colors hover:bg-blue-50"
            >
              <Edit2 size={16} />
              Change Email
            </button>
          )}
        </div>
        {!isPersistent && (
          <button
            onClick={onClose}
            className="mt-2 text-xs text-gray-400 hover:text-gray-600"
          >
            Close
          </button>
        )}
      </motion.div>
    </div>
  );
}