// Configuration de l'API
// En production, VITE_API_URL sera défini dans les variables d'environnement Netlify
export const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

console.log("🔧 API URL:", API_URL);
