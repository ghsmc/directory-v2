import React from 'react';

interface Company {
  name: string;
  logo: string;
  revenue: string;
}

const companies: Company[] = [
  { name: 'SpaceX', logo: 'https://img.logo.dev/spacex.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ', revenue: '$3.12 M' },
  { name: 'Blue Origin', logo: 'https://img.logo.dev/blueorigin.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ', revenue: '$2.84 M' },
  { name: 'Relativity Space', logo: 'https://img.logo.dev/relativityspace.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ', revenue: '$2.45 M' },
  { name: 'Planet Labs', logo: 'https://img.logo.dev/planet.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ', revenue: '$2.31 M' },
  { name: 'Rocket Lab', logo: 'https://img.logo.dev/rocketlabusa.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ', revenue: '$2.15 M' },
  { name: 'Virgin Galactic', logo: 'https://img.logo.dev/virgingalactic.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ', revenue: '$1.95 M' },
  { name: 'Astra', logo: 'https://img.logo.dev/astra.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ', revenue: '$1.82 M' },
  { name: 'Firefly Aerospace', logo: 'https://img.logo.dev/firefly.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ', revenue: '$1.76 M' },
  { name: 'ABL Space', logo: 'https://img.logo.dev/ablspacesystems.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ', revenue: '$1.64 M' },
  { name: 'Axiom Space', logo: 'https://img.logo.dev/axiomspace.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ', revenue: '$1.58 M' },
  { name: 'Vast Space', logo: 'https://img.logo.dev/vast.space?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ', revenue: '$1.45 M' },
  { name: 'Sierra Space', logo: 'https://img.logo.dev/sierraspace.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ', revenue: '$1.42 M' },
  { name: 'Astrobotic', logo: 'https://img.logo.dev/astrobotic.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ', revenue: '$1.38 M' },
  { name: 'Momentus', logo: 'https://img.logo.dev/momentus.space?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ', revenue: '$1.35 M' },
  { name: 'Varda Space', logo: 'https://img.logo.dev/varda.com?token=pk_VAZ6tvAVQHCDwKeaNRVyjQ', revenue: '$1.32 M' }
];

interface RevenueChartProps {
  isDark?: boolean;
}

export function RevenueChart({ isDark = false }: RevenueChartProps) {
  const maxRevenue = Math.max(...companies.map(c => parseFloat(c.revenue.replace(/[^0-9.]/g, ''))));

  return (
    <div className={`p-6 rounded-xl ${isDark ? 'bg-white/5' : 'bg-white'}`}>
      <h1 className={`text-2xl font-bold mb-2 ${isDark ? 'text-white' : 'text-gray-900'}`}>
        Revenue per Employee
      </h1>
      <p className={`text-sm mb-8 ${isDark ? 'text-white/60' : 'text-gray-600'}`}>
        Top SpaceTech companies
      </p>

      <div className="space-y-4">
        {companies.map((company) => {
          const percentage = (parseFloat(company.revenue.replace(/[^0-9.]/g, '')) / maxRevenue) * 100;
          
          return (
            <div key={company.name} className="flex items-center gap-4">
              <div className="w-32 flex items-center justify-between">
                <span className={`text-sm font-medium ${isDark ? 'text-white' : 'text-gray-900'}`}>
                  {company.name}
                </span>
              </div>

              <div className="w-8 h-8 flex items-center justify-center shrink-0">
                <img 
                  src={company.logo} 
                  alt={company.name}
                  className="max-w-full max-h-full object-contain"
                />
              </div>

              <div className="flex-1 relative h-8">
                <div 
                  className="absolute inset-y-0 left-0 bg-gray-600 rounded"
                  style={{ width: `${percentage}%` }}
                />
                <div className="absolute inset-y-0 right-0 flex items-center">
                  <span className={`text-sm font-medium ${isDark ? 'text-white' : 'text-gray-900'}`}>
                    {company.revenue}
                  </span>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}