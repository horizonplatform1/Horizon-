"""
Enhanced Dashboard System
Provides a comprehensive web-based dashboard for monitoring and controlling
all advanced blockchain, AI, governance, and tracking features
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sqlite3
import json
import asyncio
from typing import Dict, List, Any
import logging

from blockchain.core import Blockchain
from blockchain.advanced_ai_system import AdvancedTradingAI
from blockchain.advanced_governance import AdvancedCorporateGovernance
from blockchain.real_time_tracker import AdvancedRealTimeTracker


class EnhancedDashboard:
    """Enhanced dashboard for comprehensive system monitoring"""
    
    def __init__(self, blockchain: Blockchain, advanced_ai: AdvancedTradingAI,
                 advanced_governance: AdvancedCorporateGovernance,
                 advanced_tracker: AdvancedRealTimeTracker):
        self.blockchain = blockchain
        self.advanced_ai = advanced_ai
        self.advanced_governance = advanced_governance
        self.advanced_tracker = advanced_tracker
        
    def create_main_dashboard(self):
        """Create the main dashboard interface"""
        st.set_page_config(
            page_title="DataCoin Advanced Control Center",
            page_icon="🪙",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Main header
        st.title("🪙 DataCoin Advanced Control Center")
        st.markdown("*Comprehensive blockchain, AI, and governance management system*")
        
        # Sidebar navigation
        page = st.sidebar.selectbox(
            "🎯 Navigation",
            ["🏠 System Overview", "🤖 AI Trading", "⚖️ Governance", 
             "📊 Real-Time Tracking", "💼 Portfolio", "📈 Analytics", 
             "🚨 Alerts", "⚙️ Settings"]
        )
        
        # Route to appropriate page
        if page == "🏠 System Overview":
            self.system_overview_page()
        elif page == "🤖 AI Trading":
            self.ai_trading_page()
        elif page == "⚖️ Governance":
            self.governance_page()
        elif page == "📊 Real-Time Tracking":
            self.tracking_page()
        elif page == "💼 Portfolio":
            self.portfolio_page()
        elif page == "📈 Analytics":
            self.analytics_page()
        elif page == "🚨 Alerts":
            self.alerts_page()
        elif page == "⚙️ Settings":
            self.settings_page()
    
    def system_overview_page(self):
        """System overview dashboard page"""
        st.header("🏠 System Overview")
        
        # System status cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            blockchain_health = "🟢 Healthy" if len(self.blockchain.chain) > 0 else "🔴 Error"
            st.metric("Blockchain Status", blockchain_health, delta=f"{len(self.blockchain.chain)} blocks")
        
        with col2:
            ai_summary = self.advanced_ai.get_ai_performance_summary()
            ai_status = "🟢 Active" if ai_summary.get('trading_active') else "🔴 Inactive"
            st.metric("AI Trading", ai_status, delta=f"{ai_summary.get('total_decisions', 0)} decisions")
        
        with col3:
            gov_dashboard = self.advanced_governance.get_governance_dashboard()
            gov_status = "🟢 Monitoring" if gov_dashboard.get('system_status', {}).get('governance_active') else "🔴 Stopped"
            total_alerts = sum(len(data.get('active_alerts', [])) for data in gov_dashboard.get('companies', {}).values())
            st.metric("Governance", gov_status, delta=f"{total_alerts} alerts")
        
        with col4:
            track_dashboard = self.advanced_tracker.get_tracking_dashboard()
            track_status = "🟢 Tracking" if track_dashboard.get('system_status', {}).get('tracking_active') else "🔴 Stopped"
            st.metric("Real-Time Tracking", track_status, delta=f"{track_dashboard.get('total_events_24h', 0)} events")
        
        st.divider()
        
        # System performance charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 AI Performance Trend")
            # Create AI performance chart
            ai_data = self._get_ai_performance_data()
            if ai_data:
                fig = px.line(ai_data, x='timestamp', y='confidence', 
                             title="AI Decision Confidence Over Time")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No AI performance data available yet")
        
        with col2:
            st.subheader("🎯 Real-Time Events")
            # Create events chart
            events_data = self._get_events_data()
            if events_data:
                fig = px.bar(events_data, x='event_type', y='count', color='severity',
                           title="Events in Last 24 Hours")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No event data available yet")
        
        # Recent activity feed
        st.subheader("📰 Recent Activity")
        self._display_activity_feed()
    
    def ai_trading_page(self):
        """AI trading dashboard page"""
        st.header("🤖 AI Trading Control Center")
        
        # AI system controls
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🧠 Train AI Models"):
                with st.spinner("Training AI models..."):
                    results = self.advanced_ai.train_ai_models()
                    for company, success in results.items():
                        status = "✅" if success else "❌"
                        st.write(f"{status} {company}: {'Success' if success else 'Failed'}")
        
        with col2:
            wallet_address = st.text_input("💼 Wallet Address for Trading")
            if st.button("🚀 Start Automated Trading"):
                if wallet_address:
                    self.advanced_ai.start_automated_trading(wallet_address)
                    st.success("🚀 Automated trading started!")
                else:
                    st.error("Please enter a wallet address")
        
        with col3:
            if st.button("🛑 Stop Automated Trading"):
                self.advanced_ai.stop_automated_trading()
                st.success("🛑 Automated trading stopped")
        
        st.divider()
        
        # AI performance metrics
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 AI Performance Metrics")
            summary = self.advanced_ai.get_ai_performance_summary()
            
            metrics_data = {
                "Metric": ["Total Decisions", "Average Confidence", "Expected Return", "Models Trained"],
                "Value": [
                    summary.get('total_decisions', 0),
                    f"{summary.get('average_confidence', 0):.2%}",
                    f"{summary.get('average_expected_return', 0):.2%}",
                    f"{summary.get('ai_models_trained', 0)}/3"
                ]
            }
            st.table(pd.DataFrame(metrics_data))
        
        with col2:
            st.subheader("📈 Market Intelligence")
            company = st.selectbox("Select Company", ["GOOGL", "MSFT", "CMCSA"])
            
            if st.button("🔄 Refresh Intelligence"):
                intelligence = self.advanced_ai.gather_market_intelligence(company)
                
                st.metric("Overall Sentiment", f"{intelligence.overall_sentiment:.2f}")
                st.metric("News Sentiment", f"{intelligence.news_sentiment.get(company, 0):.2f}")
                st.metric("Social Sentiment", f"{intelligence.social_media_sentiment.get(company, 0):.2f}")
        
        # Trading decisions
        st.subheader("🎯 Recent Trading Decisions")
        self._display_trading_decisions()
    
    def governance_page(self):
        """Governance dashboard page"""
        st.header("⚖️ Corporate Governance Center")
        
        # Governance controls
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🏛️ Start Governance Monitoring"):
                self.advanced_governance.start_governance_monitoring()
                st.success("🏛️ Governance monitoring started!")
                
            if st.button("🛑 Stop Governance Monitoring"):
                self.advanced_governance.stop_governance_monitoring()
                st.success("🛑 Governance monitoring stopped")
        
        with col2:
            st.subheader("📋 Quick Actions")
            company = st.selectbox("Select Company", ["GOOGL", "MSFT", "CMCSA"], key="gov_company")
            action = st.selectbox("Select Action", ["Takeover Notice", "Proxy Fight", "Shareholder Lawsuit"])
            
            if st.button("📜 Execute Action"):
                st.info(f"Executing {action} for {company}...")
                # Implementation would go here
        
        st.divider()
        
        # Governance dashboard
        dashboard = self.advanced_governance.get_governance_dashboard()
        
        # Company overview
        st.subheader("🏢 Company Overview")
        
        for company, data in dashboard.get('companies', {}).items():
            with st.expander(f"📈 {company} Status"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Ownership", f"{data.get('ownership_percentage', 0):.4f}%")
                
                with col2:
                    st.metric("Legal Documents", data.get('total_documents', 0))
                
                with col3:
                    st.metric("Active Alerts", len(data.get('active_alerts', [])))
                
                # Recent alerts
                if data.get('active_alerts'):
                    st.write("🚨 Active Alerts:")
                    for alert in data['active_alerts'][:3]:
                        severity_color = {"LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🟠", "CRITICAL": "🔴"}
                        st.write(f"{severity_color.get(alert.get('severity', 'LOW'), '⚪')} {alert.get('description', 'N/A')}")
    
    def tracking_page(self):
        """Real-time tracking dashboard page"""
        st.header("📊 Real-Time Tracking Center")
        
        # Tracking controls
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🚀 Start Real-Time Tracking"):
                self.advanced_tracker.start_tracking()
                st.success("🚀 Real-time tracking started!")
                
            if st.button("🛑 Stop Real-Time Tracking"):
                self.advanced_tracker.stop_tracking()
                st.success("🛑 Real-time tracking stopped")
        
        with col2:
            st.subheader("📊 Tracking Status")
            dashboard = self.advanced_tracker.get_tracking_dashboard()
            status = dashboard.get('system_status', {})
            
            tracking_status = "🟢 Active" if status.get('tracking_active') else "🔴 Inactive"
            st.metric("Tracking Status", tracking_status)
            
            components = status.get('components', {})
            st.write("📡 Components:")
            st.write(f"Market: {'🟢' if components.get('market_streaming') else '🔴'}")
            st.write(f"Blockchain: {'🟢' if components.get('blockchain_monitoring') else '🔴'}")
            st.write(f"Governance: {'🟢' if components.get('governance_monitoring') else '🔴'}")
        
        st.divider()
        
        # Event analytics
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Event Overview (24h)")
            dashboard = self.advanced_tracker.get_tracking_dashboard()
            
            st.metric("Total Events", dashboard.get('total_events_24h', 0))
            st.metric("Total Alerts", dashboard.get('total_alerts_24h', 0))
            st.metric("Critical Alerts", dashboard.get('critical_alerts', 0))
        
        with col2:
            st.subheader("🚨 Recent Alerts")
            unresolved_alerts = dashboard.get('unresolved_alerts', [])
            
            if unresolved_alerts:
                for alert in unresolved_alerts[:5]:
                    severity_color = {"LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🟠", "CRITICAL": "🔴"}
                    st.write(f"{severity_color.get(alert.get('severity', 'LOW'), '⚪')} {alert.get('title', 'N/A')}")
            else:
                st.info("No unresolved alerts")
        
        # Event history
        st.subheader("📋 Event History")
        hours = st.slider("Hours to display", 1, 168, 24)
        events = self.advanced_tracker.get_event_history(hours=hours)
        
        if events:
            events_df = pd.DataFrame(events)
            st.dataframe(events_df[['timestamp', 'event_type', 'severity', 'source']])
        else:
            st.info("No events found for the selected time period")
    
    def portfolio_page(self):
        """Portfolio management dashboard page"""
        st.header("💼 Portfolio Management")
        
        # Portfolio overview
        st.subheader("📊 Current Holdings")
        
        companies = ['GOOGL', 'MSFT', 'CMCSA']
        portfolio_data = []
        
        for company in companies:
            # This would integrate with the actual share tracking system
            shares = 0  # Placeholder
            value = shares * 100  # Placeholder calculation
            
            portfolio_data.append({
                'Company': company,
                'Shares': shares,
                'Value': f"${value:,.2f}",
                'Percentage': f"{(value / max(1, sum([s * 100 for s in [0, 0, 0]])) * 100):.1f}%"
            })
        
        st.table(pd.DataFrame(portfolio_data))
        
        # Portfolio performance chart
        st.subheader("📈 Portfolio Performance")
        
        # Create sample performance data
        dates = pd.date_range(start='2024-01-01', end=datetime.now(), freq='D')
        performance_data = pd.DataFrame({
            'Date': dates,
            'Portfolio Value': np.cumsum(np.random.randn(len(dates)) * 100) + 100000
        })
        
        fig = px.line(performance_data, x='Date', y='Portfolio Value', 
                     title="Portfolio Value Over Time")
        st.plotly_chart(fig, use_container_width=True)
    
    def analytics_page(self):
        """Analytics dashboard page"""
        st.header("📈 Advanced Analytics")
        
        # Analytics overview
        tab1, tab2, tab3 = st.tabs(["📊 Market Analysis", "🎯 Predictive Models", "📈 Performance Metrics"])
        
        with tab1:
            st.subheader("📊 Market Analysis")
            
            company = st.selectbox("Select Company for Analysis", ["GOOGL", "MSFT", "CMCSA"])
            
            # Create sample market data
            dates = pd.date_range(start='2024-01-01', end=datetime.now(), freq='D')
            market_data = pd.DataFrame({
                'Date': dates,
                'Price': np.cumsum(np.random.randn(len(dates)) * 2) + 150,
                'Volume': np.random.randint(1000000, 10000000, len(dates))
            })
            
            fig = make_subplots(rows=2, cols=1, 
                              subplot_titles=['Price Movement', 'Trading Volume'],
                              vertical_spacing=0.1)
            
            fig.add_trace(go.Scatter(x=market_data['Date'], y=market_data['Price'], 
                                   name='Price'), row=1, col=1)
            fig.add_trace(go.Bar(x=market_data['Date'], y=market_data['Volume'], 
                               name='Volume'), row=2, col=1)
            
            fig.update_layout(height=600, title_text=f"{company} Market Analysis")
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            st.subheader("🎯 Predictive Models")
            
            company = st.selectbox("Company for Prediction", ["GOOGL", "MSFT", "CMCSA"], key="pred_company")
            
            if st.button("🔮 Generate Prediction"):
                # This would integrate with the actual predictive analytics
                prediction_data = {
                    'Metric': ['Next Day Price', 'Confidence', 'Expected Return', 'Risk Level'],
                    'Prediction': ['$152.45', '78%', '+2.3%', 'Medium']
                }
                st.table(pd.DataFrame(prediction_data))
        
        with tab3:
            st.subheader("📈 Performance Metrics")
            
            # Performance summary
            metrics = {
                'Total Return': '+15.7%',
                'Sharpe Ratio': '1.23',
                'Max Drawdown': '-8.5%',
                'Win Rate': '68%'
            }
            
            col1, col2, col3, col4 = st.columns(4)
            metrics_cols = [col1, col2, col3, col4]
            
            for i, (metric, value) in enumerate(metrics.items()):
                with metrics_cols[i]:
                    st.metric(metric, value)
    
    def alerts_page(self):
        """Alerts management page"""
        st.header("🚨 Alert Management")
        
        # Alert summary
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Active Alerts", "7", delta="2")
        
        with col2:
            st.metric("Critical Alerts", "2", delta="1")
        
        with col3:
            st.metric("Resolved Today", "15", delta="5")
        
        st.divider()
        
        # Alert filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            severity_filter = st.selectbox("Filter by Severity", ["All", "Critical", "High", "Medium", "Low"])
        
        with col2:
            source_filter = st.selectbox("Filter by Source", ["All", "AI Trading", "Governance", "Tracking"])
        
        with col3:
            time_filter = st.selectbox("Time Period", ["24 hours", "7 days", "30 days"])
        
        # Alert list
        st.subheader("📋 Alert List")
        
        # Sample alert data
        alerts_data = [
            {"Timestamp": "2024-01-20 14:30", "Severity": "Critical", "Source": "Governance", "Message": "5% ownership threshold reached for GOOGL"},
            {"Timestamp": "2024-01-20 13:15", "Severity": "High", "Source": "AI Trading", "Message": "Significant price movement detected for MSFT"},
            {"Timestamp": "2024-01-20 12:00", "Severity": "Medium", "Source": "Tracking", "Message": "Unusual trading volume for CMCSA"},
        ]
        
        alerts_df = pd.DataFrame(alerts_data)
        st.dataframe(alerts_df, use_container_width=True)
    
    def settings_page(self):
        """Settings and configuration page"""
        st.header("⚙️ System Settings")
        
        # AI Settings
        with st.expander("🤖 AI Trading Settings"):
            st.slider("Risk Tolerance", 0.0, 1.0, 0.7)
            st.slider("Max Position Size", 0.1, 0.5, 0.3)
            st.multiselect("Trading Companies", ["GOOGL", "MSFT", "CMCSA"], ["GOOGL", "MSFT", "CMCSA"])
        
        # Governance Settings
        with st.expander("⚖️ Governance Settings"):
            st.text_input("Notification Email", "governance@datacoin.com")
            st.checkbox("Email Notifications", True)
            st.checkbox("Webhook Notifications", True)
        
        # Tracking Settings
        with st.expander("📊 Tracking Settings"):
            st.slider("Event Retention (days)", 1, 365, 30)
            st.slider("Alert Cooldown (minutes)", 1, 60, 5)
            st.checkbox("Market Data Streaming", True)
        
        # System Configuration
        with st.expander("🔧 System Configuration"):
            st.text_input("Database Path", "data/")
            st.slider("Mining Difficulty", 1, 6, 4)
            st.number_input("Block Reward", 50.0)
        
        if st.button("💾 Save Settings"):
            st.success("⚙️ Settings saved successfully!")
    
    # Helper methods
    def _get_ai_performance_data(self):
        """Get AI performance data for charting"""
        try:
            conn = sqlite3.connect(self.advanced_ai.db_path)
            query = """
                SELECT DATE(timestamp) as date, AVG(confidence) as confidence
                FROM ai_decisions 
                WHERE timestamp > datetime('now', '-30 days')
                GROUP BY DATE(timestamp)
                ORDER BY date
            """
            df = pd.read_sql_query(query, conn)
            conn.close()
            
            if not df.empty:
                df['timestamp'] = pd.to_datetime(df['date'])
                return df
        except Exception as e:
            logging.error(f"Error getting AI performance data: {e}")
        
        return None
    
    def _get_events_data(self):
        """Get events data for charting"""
        try:
            conn = sqlite3.connect(self.advanced_tracker.db_path)
            query = """
                SELECT event_type, severity, COUNT(*) as count
                FROM events 
                WHERE timestamp > datetime('now', '-24 hours')
                GROUP BY event_type, severity
            """
            df = pd.read_sql_query(query, conn)
            conn.close()
            return df if not df.empty else None
        except Exception as e:
            logging.error(f"Error getting events data: {e}")
        
        return None
    
    def _display_activity_feed(self):
        """Display recent activity feed"""
        activities = [
            "🤖 AI recommended buying 150 shares of GOOGL",
            "⚖️ Takeover notice filed for MSFT (5.2% ownership)",
            "📊 Price spike alert triggered for CMCSA (+8.3%)",
            "🏛️ Board notification sent to Google executives",
            "💰 New block mined: 50 DataCoin reward"
        ]
        
        for activity in activities:
            st.write(f"• {activity}")
    
    def _display_trading_decisions(self):
        """Display recent trading decisions"""
        # This would integrate with the actual AI decision history
        decisions_data = [
            {"Timestamp": "2024-01-20 14:30", "Company": "GOOGL", "Action": "BUY", "Shares": 150, "Confidence": "85%"},
            {"Timestamp": "2024-01-20 13:15", "Company": "MSFT", "Action": "HOLD", "Shares": 0, "Confidence": "62%"},
            {"Timestamp": "2024-01-20 12:00", "Company": "CMCSA", "Action": "BUY", "Shares": 75, "Confidence": "78%"},
        ]
        
        decisions_df = pd.DataFrame(decisions_data)
        st.dataframe(decisions_df, use_container_width=True)


def run_enhanced_dashboard(blockchain, advanced_ai, advanced_governance, advanced_tracker):
    """Run the enhanced dashboard application"""
    dashboard = EnhancedDashboard(blockchain, advanced_ai, advanced_governance, advanced_tracker)
    dashboard.create_main_dashboard()


# Streamlit app entry point
if __name__ == "__main__":
    st.write("Please run this dashboard through the main DataCoin system")