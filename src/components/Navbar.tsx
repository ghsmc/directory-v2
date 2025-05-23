import { Link, useLocation } from 'react-router-dom';
import { AlignLeft, Briefcase, Building2, Users2, MessageSquare } from 'lucide-react';

export function Navbar() {
  const location = useLocation();
  
  const links = [
    { path: '/feed', label: 'Feed', icon: AlignLeft },
    { path: '/jobs', label: 'Jobs', icon: Briefcase },
    { 
      path: '/chat', 
      label: 'Chat',
      customIcon: (
        <img 
          src="/logo.png"
          alt="Milo"
          className="w-12 h-12 rounded-lg object-contain"
        />
      )
    },
    { path: '/companies', label: 'Companies', icon: Building2 },
    { path: '/people', label: 'People', icon: Users2 }
  ];

  return (
    <>
      {/* Desktop Sidebar */}
      <nav className="hidden md:flex fixed left-0 top-0 bottom-0 w-[72px] bg-white border-r border-gray-100 flex-col items-center py-4 z-50">
        {/* Logo */}
        <Link to="/" className="mb-8">
          <img 
            src="/logo.png"
            alt="Milo"
            className="w-24 h-24 rounded-xl object-contain"
          />
        </Link>

        {/* Navigation Links */}
        <div className="flex-1 flex flex-col items-center gap-1">
          {links.map((link) => {
            const Icon = link.icon;
            const isActive = location.pathname === link.path;
            
            return (
              <Link
                key={link.path}
                to={link.path}
                className={`
                  relative w-full flex flex-col items-center gap-1 py-3 px-1 group
                  ${isActive 
                    ? 'text-emerald-500 bg-emerald-50' 
                    : 'text-gray-400 hover:text-emerald-500'
                  }
                `}
              >
                {link.customIcon || (Icon && <Icon size={24} />)}
                <span className="text-[10px] font-medium leading-none">{link.label}</span>
                {isActive && (
                  <div className="absolute left-0 top-0 bottom-0 w-[3px] bg-emerald-500" />
                )}
              </Link>
            );
          })}
        </div>

        {/* Bottom Icons */}
        <div className="mt-auto flex flex-col items-center gap-3">
          <button className="w-[42px] h-[42px] flex items-center justify-center rounded-[14px] bg-gray-50/80">
            <div className="w-[22px] h-[22px] rounded-full bg-gray-300" />
          </button>
        </div>
      </nav>

      {/* Mobile Bottom Navigation */}
      <nav className="md:hidden fixed bottom-0 inset-x-0 bg-white border-t border-gray-100 z-50">
        <div className="grid grid-cols-5 h-[72px] pb-safe">
          {links.map((link) => {
            const Icon = link.icon;
            const isActive = location.pathname === link.path;
            
            return (
              <Link
                key={link.path}
                to={link.path}
                className={`
                  flex flex-col items-center justify-center gap-1
                  ${isActive 
                    ? 'text-emerald-500' 
                    : 'text-gray-400 hover:text-emerald-500'
                  }
                `}
              >
                {link.customIcon || (Icon && <Icon size={24} />)}
                <span className="text-[10px] font-medium leading-none">{link.label}</span>
              </Link>
            );
          })}
        </div>
      </nav>
    </>
  );
}