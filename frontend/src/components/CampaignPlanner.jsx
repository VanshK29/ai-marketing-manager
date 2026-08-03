import { useState } from 'react';

const API_URL = 'http://localhost:8000/api';

export default function CampaignPlanner() {
  const [industry, setIndustry] = useState('');
  const [campaignFocus, setCampaignFocus] = useState('');
  const [loading, setLoading] = useState(false);
  const [plan, setPlan] = useState(null);
  const [error, setError] = useState(null);
  const [contentLoading, setContentLoading] = useState(false);
  const [contentPlan, setContentPlan] = useState(null);
  const [optimizeLoading, setOptimizeLoading] = useState(false);
  const [optimizeReport, setOptimizeReport] = useState(null);

  const generatePlan = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setPlan(null);
    setContentPlan(null);
    setOptimizeReport(null);
    try {
      const res = await fetch(`${API_URL}/plan`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ industry, campaign_focus: campaignFocus })
      });
      if (!res.ok) throw new Error("Failed to generate plan");
      const data = await res.json();
      setPlan(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const generateContent = async () => {
    setContentLoading(true);
    try {
      const res = await fetch(`${API_URL}/content`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ campaign_plan: plan })
      });
      if (!res.ok) throw new Error("Failed to generate content");
      const data = await res.json();
      setContentPlan(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setContentLoading(false);
    }
  };

  const generateOptimization = async () => {
    setOptimizeLoading(true);
    try {
      const res = await fetch(`${API_URL}/optimize`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ campaign_name: plan?.campaign_name || campaignFocus || 'Marketing Campaign' })
      });
      if (!res.ok) throw new Error("Failed to optimize campaign");
      const data = await res.json();
      setOptimizeReport(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setOptimizeLoading(false);
    }
  };

  return (
    <div className="glass-card" style={{ animationDelay: '0.2s' }}>
      <h2>1. Campaign Strategy</h2>
      <p className="subtitle" style={{ marginBottom: '1.5rem', fontSize: '1rem' }}>
        Define your industry and goal, and our agents will research competitors and build a plan.
      </p>
      
      <form onSubmit={generatePlan}>
        <div className="form-group">
          <label className="form-label">Industry</label>
          <input 
            type="text" 
            className="input-field" 
            placeholder="e.g. Eco-friendly footwear"
            value={industry}
            onChange={(e) => setIndustry(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label className="form-label">Campaign Focus</label>
          <input 
            type="text" 
            className="input-field" 
            placeholder="e.g. Summer launch targeting Gen-Z"
            value={campaignFocus}
            onChange={(e) => setCampaignFocus(e.target.value)}
            required
          />
        </div>
        <button type="submit" className="btn-primary" disabled={loading || contentLoading}>
          {loading ? <span className="loading-spinner"></span> : null}
          {loading ? 'Agents are researching...' : 'Generate Campaign Plan'}
        </button>
      </form>

      {error && <p style={{color: '#ef4444', marginTop: '1rem'}}>{error}</p>}

      {plan && (
        <div className="result-section" style={{animation: 'fadeInUp 0.5s ease-out'}}>
          <h3 style={{marginBottom: '1rem', color: 'var(--accent-primary)'}}>Generated Plan</h3>
          <pre>{JSON.stringify(plan, null, 2)}</pre>
          
          {!contentPlan && (
            <div style={{marginTop: '1.5rem', padding: '1.5rem', background: 'rgba(59, 130, 246, 0.1)', borderRadius: '8px', border: '1px solid rgba(59, 130, 246, 0.3)'}}>
              <h4 style={{marginBottom: '0.5rem'}}>Human Approval Required</h4>
              <p style={{fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '1rem'}}>
                Please review the campaign plan above. If approved, the Content Strategist agent will proceed to generate the content calendar.
              </p>
              <button 
                className="btn-primary" 
                style={{background: 'linear-gradient(135deg, #10b981, #059669)'}}
                onClick={generateContent}
                disabled={contentLoading}
              >
                {contentLoading ? <span className="loading-spinner"></span> : null}
                {contentLoading ? 'Strategizing Content...' : 'Approve & Generate Content'}
              </button>
            </div>
          )}
        </div>
      )}

      {contentPlan && (
        <div className="result-section" style={{animation: 'fadeInUp 0.5s ease-out', marginTop: '2rem'}}>
          <h3 style={{marginBottom: '1rem', color: 'var(--accent-secondary)'}}>Content Calendar</h3>
          <pre>{JSON.stringify(contentPlan, null, 2)}</pre>
          
          {!optimizeReport && (
            <div style={{marginTop: '1.5rem', padding: '1.5rem', background: 'rgba(168, 85, 247, 0.1)', borderRadius: '8px', border: '1px solid rgba(168, 85, 247, 0.3)'}}>
              <h4 style={{marginBottom: '0.5rem'}}>3. Optimization & Analytics Advisory</h4>
              <p style={{fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '1rem'}}>
                Send your live campaign to the Analytics Specialist & Optimization Advisor agents to generate performance insights.
              </p>
              <button 
                className="btn-primary" 
                style={{background: 'linear-gradient(135deg, #8b5cf6, #7c3aed)'}}
                onClick={generateOptimization}
                disabled={optimizeLoading}
              >
                {optimizeLoading ? <span className="loading-spinner"></span> : null}
                {optimizeLoading ? 'Analyzing Performance...' : 'Run Campaign Optimization'}
              </button>
            </div>
          )}
        </div>
      )}

      {optimizeReport && (
        <div className="result-section" style={{animation: 'fadeInUp 0.5s ease-out', marginTop: '2rem'}}>
          <h3 style={{marginBottom: '1rem', color: '#a855f7'}}>Optimization Report</h3>
          <pre>{typeof optimizeReport.optimization_report === 'string' ? optimizeReport.optimization_report : JSON.stringify(optimizeReport, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
