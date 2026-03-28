/**
 * CRO Scheduler - Automação de Análises
 * Versão Node.js
 */

import schedule from 'node-schedule';
import { CROAnalyzer } from '../src/lib/analyzer.js';
import { createClient } from '@supabase/supabase-js';
import dotenv from 'dotenv';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

dotenv.config();

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const SUPABASE_URL = process.env.SUPABASE_URL;
const SUPABASE_SERVICE_KEY = process.env.SUPABASE_SERVICE_KEY;
const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_KEY);

class CROScheduler {
  constructor() {
    this.analyzer = new CROAnalyzer();
    this.jobs = [];
    this.scheduling = false;
  }

  /**
   * Executa análise completa
   */
  async runAnalysis(source = 'auto') {
    console.log(`\n⏱️  Iniciando análise [${source}] - ${new Date().toLocaleString('pt-BR')}`);

    try {
      // Fetch dados do Supabase
      const { data: csvData, error: csvError } = await supabase
        .storage
        .from('analysis-data')
        .download('sample_data.csv');

      if (csvError) {
        console.warn('⚠️  CSV não encontrado, criando dados mock');
        const mockData = this.generateMockData();
        try {
          await this.saveAnalysis(mockData, source);
          return mockData;
        } catch (saveError) {
          console.error('❌ Erro ao salvar análise:', saveError.message);
          return null;
        }
      }

      // Parse CSV
      const csvText = await csvData.text();
      const events = this.parseCSV(csvText);

      // Executar análise
      const results = this.analyzer.analyze(events, [
        'page_view',
        'view_item',
        'add_to_cart',
        'begin_checkout',
        'purchase'
      ]);

      // Salvar resultados
      await this.saveAnalysis(results, source);

      console.log(`✅ Análise concluída`);
      console.log(`   Taxa de conversão: ${results.total_conversion_rate.toFixed(2)}%`);
      console.log(`   Pontos de abandono: ${results.abandonment_points.length}`);
      console.log(`   Recomendações: ${results.recommendations.length}`);

      return results;
    } catch (error) {
      console.error(`❌ Erro na análise:`, error.message);
      return null;
    }
  }

  /**
   * Salva resultados no Supabase
   */
  async saveAnalysis(results, source = 'auto') {
    try {
      const { data, error } = await supabase
        .from('cro_reports')
        .insert([{
          analysis_data: results.funnel_analysis || results,
          funnel_steps: results.funnel_analysis?.funnel_steps || [],
          metrics: {
            conversion_rate: results.total_conversion_rate,
            abandonment_points: results.abandonment_points?.length || 0,
            recommendations: results.recommendations?.length || 0
          },
          recommendations: results.recommendations || [],
          summary: `Análise automática - ${new Date().toLocaleString('pt-BR')}`,
          source: source,
          created_at: new Date().toISOString()
        }])
        .select()
        .single();

      if (error) {
        console.warn('⚠️  Erro ao salvar no Supabase:', error.message);
        console.log('   Salvando localmente em reports_auto/');
        this.saveLocal(results);
      } else {
        console.log(`✅ Salvo no Supabase com ID: ${data.id}`);
      }

      return data;
    } catch (error) {
      console.error('❌ Erro ao salvar resultados:', error.message);
      this.saveLocal(results);
    }
  }

  /**
   * Salva análise localmente (fallback)
   */
  saveLocal(results) {
    try {
      const dir = path.join(__dirname, '../reports_auto');
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }

      const timestamp = new Date().toISOString().replace(/[:.]/g, '-').split('T')[0];
      const filename = `analysis_${timestamp}.json`;
      const filepath = path.join(dir, filename);

      fs.writeFileSync(filepath, JSON.stringify(results, null, 2));
      console.log(`✅ Salvo localmente: ${filepath}`);
    } catch (error) {
      console.error('❌ Erro ao salvar localmente:', error.message);
    }
  }

  /**
   * Parse CSV para eventos
   */
  parseCSV(csvText) {
    const lines = csvText.trim().split('\n');
    const headers = lines[0].split(',');

    return lines.slice(1).map(line => {
      const values = line.split(',');
      const event = {};

      headers.forEach((header, index) => {
        event[header.trim()] = values[index]?.trim() || '';
      });

      return event;
    });
  }

  /**
   * Gera dados mock para testes
   */
  generateMockData() {
    const events = [];
    const userId = () => `user_${Math.floor(Math.random() * 150)}`;
    const timestamp = () => new Date(Date.now() - Math.random() * 86400000).toISOString();

    const eventNames = ['page_view', 'view_item', 'add_to_cart', 'begin_checkout', 'purchase'];

    for (let i = 0; i < 350; i++) {
      const stepIndex = Math.floor(Math.random() * eventNames.length);
      
      // Simular abandono progressivo
      let includeEvent = true;
      if (stepIndex === 1) includeEvent = Math.random() > 0.1;
      if (stepIndex === 2) includeEvent = Math.random() > 0.3;
      if (stepIndex === 3) includeEvent = Math.random() > 0.5;
      if (stepIndex === 4) includeEvent = Math.random() > 0.94;

      if (includeEvent) {
        events.push({
          user_id: userId(),
          event_name: eventNames[stepIndex],
          timestamp: timestamp(),
          event_id: `evt_${i}`
        });
      }
    }

    const analyzer = new CROAnalyzer();
    return analyzer.analyze(events, eventNames);
  }

  /**
   * Agenda análise diária
   */
  scheduleDaily(hour = 2, minute = 0) {
    const cronExpression = `${minute} ${hour} * * *`;
    
    const job = schedule.scheduleJob(cronExpression, async () => {
      console.log(`\n🔔 Análise diária acionada às ${hour}:${String(minute).padStart(2, '0')}`);
      await this.runAnalysis('scheduled-daily');
    });

    this.jobs.push(job);
    console.log(`📅 Análise agendada: Diariamente às ${hour}:${String(minute).padStart(2, '0')}`);

    return job;
  }

  /**
   * Agenda análise horária
   */
  scheduleHourly() {
    const job = schedule.scheduleJob('0 * * * *', async () => {
      console.log(`\n🔔 Análise horária acionada`);
      await this.runAnalysis('scheduled-hourly');
    });

    this.jobs.push(job);
    console.log(`📅 Análise agendada: A cada hora`);

    return job;
  }

  /**
   * Agenda análise semanal
   */
  scheduleWeekly(dayOfWeek = 1, hour = 2, minute = 0) {
    const daysOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    const day = daysOfWeek[dayOfWeek];
    const cronExpression = `${minute} ${hour} * * ${dayOfWeek}`;

    const job = schedule.scheduleJob(cronExpression, async () => {
      console.log(`\n🔔 Análise semanal acionada (${day})`);
      await this.runAnalysis('scheduled-weekly');
    });

    this.jobs.push(job);
    console.log(`📅 Análise agendada: ${day}s às ${hour}:${String(minute).padStart(2, '0')}`);

    return job;
  }

  /**
   * Inicia daemon de scheduling
   */
  startDaemon() {
    this.scheduling = true;
    console.log('\n🚀 CRO Scheduler iniciado');
    console.log('   (Pressione Ctrl+C para parar)');
  }

  /**
   * Para todos os jobs
   */
  stopAll() {
    console.log('\n⏹️  Parando scheduler...');
    for (const job of this.jobs) {
      job.cancel();
    }
    this.scheduling = false;
    console.log('✅ Scheduler parado');
  }

  /**
   * Lista jobs agendados
   */
  listSchedules() {
    console.log(`\n📋 Jobs agendados: ${this.jobs.length}`);
    this.jobs.forEach((job, index) => {
      console.log(`   ${index + 1}. ${job.nextInvocation().toString()}`);
    });
  }
}

// CLI Interface
async function main() {
  const scheduler = new CROScheduler();
  const args = process.argv.slice(2);

  if (args[0] === '--run') {
    // Executar uma vez
    await scheduler.runAnalysis('manual');
  } else if (args[0] === '--daily') {
    // Diário
    const hour = parseInt(args[1]) || 2;
    scheduler.scheduleDaily(hour);
    scheduler.startDaemon();
  } else if (args[0] === '--hourly') {
    // A cada hora
    scheduler.scheduleHourly();
    scheduler.startDaemon();
  } else if (args[0] === '--weekly') {
    // Semanal
    const day = parseInt(args[1]) || 1;
    scheduler.scheduleWeekly(day);
    scheduler.startDaemon();
  } else {
    // Menu interativo
    console.log('\n🤖 CRO Scheduler - Node.js Edition');
    console.log('\nOpções:');
    console.log('  npm run schedule -- --run          Executar análise agora');
    console.log('  npm run schedule -- --daily 2      Agendar diário às 2 AM');
    console.log('  npm run schedule -- --hourly       Agendar a cada hora');
    console.log('  npm run schedule -- --weekly 1     Agendar semanalmente (1=Monday)');
  }

  // Graceful shutdown
  process.on('SIGINT', () => {
    scheduler.stopAll();
    process.exit(0);
  });
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch(console.error);
}

export { CROScheduler };
