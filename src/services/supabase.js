//Inicializamos supabase y exportar el cliente
import { createClient } from '@supabase/supabase-js';

const SUPABASE_URL = 'https://xlyfdgnpjpnrydqlnjzr.supabase.co';
const SUPABASE_KEY = 'sb_publishable_dia_1rJMZWGMKRAlzq068w_UVVeeG8m';

export const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);