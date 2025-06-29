export const isValidEmail = (email: string) => {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
};

export const isValidLinkedInUrl = (url: string) => {
  if (!url) return true; // Optional field
  return /^https?:\/\/(www\.)?linkedin\.com\/in\/[\w-]+\/?$/.test(url);
};

export const validatePassword = (password: string) => {
  if (!password) return { isValid: false, message: 'Please enter your password' };
  if (password.length < 6) return { isValid: false, message: 'Password must be at least 6 characters' };
  return { isValid: true, message: '' };
};

export const validateEmail = (email: string) => {
  if (!email) return { isValid: false, message: 'Please enter your email' };
  if (!isValidEmail(email)) return { isValid: false, message: 'Please enter a valid email address' };
  return { isValid: true, message: '' };
};

export const validateLinkedInUrl = (url: string) => {
  if (!url) return { isValid: true, message: '' }; // Optional field
  if (!isValidLinkedInUrl(url)) return { isValid: false, message: 'Please enter a valid LinkedIn URL' };
  return { isValid: true, message: '' };
};

export const validateRequired = (value: string, fieldName: string) => {
  if (!value) return { isValid: false, message: `Please enter your ${fieldName}` };
  return { isValid: true, message: '' };
}; 