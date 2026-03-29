/**
 * Authentication Middleware
 * 
 * Verifica se o usuário está autenticado antes de acessar endpoints protegidos
 */

export async function verifyToken(req, res, next) {
  try {
    const authHeader = req.headers.authorization;

    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return res.status(401).json({
        error: 'Autorização necessária',
        message: 'Inclua Authorization: Bearer {token} no header'
      });
    }

    const token = authHeader.substring(7); // Remove "Bearer "

    if (!token) {
      return res.status(401).json({
        error: 'Token ausente',
      });
    }

    // TODO: Validar token com Supabase
    // const { data, error } = await supabase.auth.getUser(token);
    // if (error) return res.status(401).json({ error: 'Token inválido' });

    // Por enquanto, apenas verifica se existe
    req.token = token;
    next();
  } catch (error) {
    console.error('Erro na autenticação:', error);
    res.status(500).json({ error: 'Erro ao verificar autenticação' });
  }
}

export default { verifyToken };
