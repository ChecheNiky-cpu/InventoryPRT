import { useState } from 'react';
import { LoginScreen } from './components/LoginScreen';
import { InventoryDashboard } from './components/InventoryDashboard';

export default function App() {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [username, setUsername] = useState('');

    const handleLogin = (user: string, password: string) => {
        // Mock login - en producción esto se validaría con un backend
        if (user && password) {
            setIsLoggedIn(true);
            setUsername(user);
        }
    };

    const handleLogout = () => {
        setIsLoggedIn(false);
        setUsername('');
    };

    return (
        <div className="min-h-screen bg-gray-50">
            {!isLoggedIn ? (
                <LoginScreen onLogin={handleLogin} />
            ) : (
                <InventoryDashboard onLogout={handleLogout} username={username} />
            )}
        </div>
    );
}
