import React, { useState } from 'react';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Card, CardContent } from '@/components/ui/card';
import { Search, Github, Globe, Twitter, Filter, BarChart2 } from 'lucide-react';

const TIERS = ['S', 'A', 'B', 'C', 'D'];
const ROLES = ['Tank', 'DPS', 'Support'];

const Header = () => (
  <div className="fixed top-0 left-0 right-0 bg-gray-900/95 backdrop-blur-sm border-b border-gray-800 z-50">
    <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
      <div className="flex items-center space-x-8">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 bg-gradient-to-br from-purple-500 to-pink-500 rounded-lg" />
          <span className="text-xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent">
            Best Brawl
          </span>
        </div>
        <nav className="hidden md:flex space-x-6">
          <a href="#" className="text-gray-400 hover:text-white transition-colors">Home</a>
          <a href="#" className="text-gray-400 hover:text-white transition-colors">Tier List</a>
          <a href="#" className="text-gray-400 hover:text-white transition-colors">Statistics</a>
          <a href="#" className="text-gray-400 hover:text-white transition-colors">Meta</a>
        </nav>
      </div>
      <div className="flex items-center space-x-4">
        <button className="p-2 text-gray-400 hover:text-white transition-colors">
          <Github className="w-5 h-5" />
        </button>
        <button className="p-2 text-gray-400 hover:text-white transition-colors">
          <Twitter className="w-5 h-5" />
        </button>
      </div>
    </div>
  </div>
);

const Footer = () => (
  <footer className="mt-auto bg-gray-900/95 backdrop-blur-sm border-t border-gray-800">
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
        <div>
          <h3 className="font-bold mb-4">Best Brawl</h3>
          <p className="text-sm text-gray-400">
            Real-time Brawl Stars statistics and tier lists, updated hourly with data from millions of matches.
          </p>
        </div>
        <div>
          <h3 className="font-bold mb-4">Resources</h3>
          <ul className="space-y-2 text-sm text-gray-400">
            <li><a href="#" className="hover:text-white transition-colors">API</a></li>
            <li><a href="#" className="hover:text-white transition-colors">Documentation</a></li>
            <li><a href="#" className="hover:text-white transition-colors">Support</a></li>
          </ul>
        </div>
        <div>
          <h3 className="font-bold mb-4">Connect</h3>
          <ul className="space-y-2 text-sm text-gray-400">
            <li>
              <a href="#" className="flex items-center space-x-2 hover:text-white transition-colors">
                <Github className="w-4 h-4" />
                <span>GitHub</span>
              </a>
            </li>
            <li>
              <a href="#" className="flex items-center space-x-2 hover:text-white transition-colors">
                <Twitter className="w-4 h-4" />
                <span>Twitter</span>
              </a>
            </li>
            <li>
              <a href="#" className="flex items-center space-x-2 hover:text-white transition-colors">
                <Globe className="w-4 h-4" />
                <span>Website</span>
              </a>
            </li>
          </ul>
        </div>
        <div>
          <h3 className="font-bold mb-4">About</h3>
          <ul className="space-y-2 text-sm text-gray-400">
            <li><a href="#" className="hover:text-white transition-colors">Team</a></li>
            <li><a href="#" className="hover:text-white transition-colors">Privacy</a></li>
            <li><a href="#" className="hover:text-white transition-colors">Terms</a></li>
          </ul>
        </div>
      </div>
      <div className="mt-8 pt-8 border-t border-gray-800 text-center text-sm text-gray-400">
        <p>© 2024 Best Brawl. All rights reserved.</p>
      </div>
    </div>
  </footer>
);

const BrawlerCard = ({ name, role, winRate, pickRate, tier }) => (
  <div className="group relative w-24 h-24 bg-gray-800 rounded-lg overflow-hidden hover:ring-2 hover:ring-blue-400 transition-all cursor-pointer">
    <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
    <div className="w-8 h-8 bg-purple-500 rounded-full m-2" /> {/* Placeholder for brawler image */}
    <div className="absolute bottom-0 left-0 right-0 p-2">
      <div className="text-sm font-bold truncate">{name}</div>
      <div className="text-xs text-gray-300">{role}</div>
    </div>

    {/* Hover tooltip */}
    <div className="absolute hidden group-hover:block top-full mt-2 left-1/2 -translate-x-1/2 w-64 p-4 bg-gray-900 rounded-lg shadow-xl z-50">
      <div className="text-lg font-bold mb-3">{name}</div>
      <div className="space-y-2">
        <div className="flex justify-between items-center">
          <span className="text-gray-400">Win Rate</span>
          <div className="flex items-center">
            <div className="w-32 h-2 bg-gray-800 rounded-full overflow-hidden mr-2">
              <div
                className="h-full bg-green-500 rounded-full"
                style={{ width: `${winRate}%` }}
              />
            </div>
            <span>{winRate}%</span>
          </div>
        </div>
        <div className="flex justify-between items-center">
          <span className="text-gray-400">Pick Rate</span>
          <div className="flex items-center">
            <div className="w-32 h-2 bg-gray-800 rounded-full overflow-hidden mr-2">
              <div
                className="h-full bg-blue-500 rounded-full"
                style={{ width: `${pickRate}%` }}
              />
            </div>
            <span>{pickRate}%</span>
          </div>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-400">Role</span>
          <span>{role}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-gray-400">Tier</span>
          <span>{tier}</span>
        </div>
      </div>
    </div>
  </div>
);

const TierRow = ({ tier, brawlers }) => (
  <div className="flex items-stretch gap-4 mb-4 group">
    <div className={`
      flex items-center justify-center w-16 rounded-lg font-bold text-3xl
      ${tier === 'S' ? 'bg-red-500/20 text-red-500' :
        tier === 'A' ? 'bg-orange-500/20 text-orange-500' :
        tier === 'B' ? 'bg-yellow-500/20 text-yellow-500' :
        tier === 'C' ? 'bg-green-500/20 text-green-500' :
        'bg-blue-500/20 text-blue-500'}
    `}>
      {tier}
    </div>
    <div className="flex-1 bg-gray-800/30 rounded-lg p-4 group-hover:bg-gray-800/40 transition-colors">
      <div className="flex flex-wrap gap-4">
        {brawlers.map(brawler => (
          <BrawlerCard key={brawler.name} {...brawler} tier={tier} />
        ))}
      </div>
    </div>
  </div>
);

const FilterBar = ({ onFilterChange }) => (
  <div className="flex items-center space-x-4 mb-6 p-4 bg-gray-800/30 rounded-lg">
    <Filter className="w-5 h-5 text-gray-400" />
    <div className="flex space-x-2">
      {ROLES.map(role => (
        <button
          key={role}
          className="px-3 py-1 text-sm rounded-full bg-gray-700 hover:bg-gray-600 transition-colors"
          onClick={() => onFilterChange(role)}
        >
          {role}
        </button>
      ))}
    </div>
  </div>
);

const App = () => {
  const [selectedMode, setSelectedMode] = useState('');
  const [selectedMap, setSelectedMap] = useState('');
  const [searchQuery, setSearchQuery] = useState('');

  // Sample data - expanded for many brawlers
  const mockBrawlers = TIERS.reduce((acc, tier) => {
    acc[tier] = Array(tier === 'S' ? 6 : 15).fill(null).map((_, i) => ({
      name: `Brawler ${tier}${i + 1}`,
      role: ROLES[i % ROLES.length],
      winRate: 45 + Math.random() * 10,
      pickRate: 5 + Math.random() * 10
    }));
    return acc;
  }, {});

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col">
      <Header />

      <main className="flex-1 max-w-7xl mx-auto px-4 py-24">
        <div className="mb-8 space-y-4">
          <div className="flex justify-between items-start">
            <div>
              <h1 className="text-4xl font-bold">
                Brawl Stars Tier List
              </h1>
              <p className="text-gray-400 mt-2">
                Updated hourly with data from millions of matches
              </p>
            </div>
            <div className="flex space-x-2">
              <button className="p-2 bg-gray-800 rounded-lg hover:bg-gray-700 transition-colors">
                <BarChart2 className="w-5 h-5" />
              </button>
              <button className="p-2 bg-gray-800 rounded-lg hover:bg-gray-700 transition-colors">
                <Filter className="w-5 h-5" />
              </button>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Select value={selectedMode} onValueChange={setSelectedMode}>
              <SelectTrigger>
                <SelectValue placeholder="Select Mode" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="bounty">Bounty</SelectItem>
                <SelectItem value="brawlBall">Brawl Ball</SelectItem>
              </SelectContent>
            </Select>

            <Select value={selectedMap} onValueChange={setSelectedMap}>
              <SelectTrigger>
                <SelectValue placeholder="Select Map" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="map1">Map 1</SelectItem>
                <SelectItem value="map2">Map 2</SelectItem>
              </SelectContent>
            </Select>

            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search brawlers..."
                className="w-full h-10 pl-10 bg-gray-800 rounded-md border border-gray-700 focus:ring-2 focus:ring-blue-400 focus:border-transparent"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>
          </div>
        </div>

        <FilterBar onFilterChange={(role) => console.log('Filter by:', role)} />

        <Card className="bg-gray-800/50 border-gray-700">
          <CardContent className="p-6">
            {TIERS.map(tier => (
              <TierRow key={tier} tier={tier} brawlers={mockBrawlers[tier]} />
            ))}
          </CardContent>
        </Card>
      </main>

      <Footer />
    </div>
  );
};

export default App;