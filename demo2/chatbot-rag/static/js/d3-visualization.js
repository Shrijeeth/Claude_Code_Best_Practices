// D3.js Chat Analytics Visualization

class ChatAnalytics {
    constructor(containerId) {
        this.containerId = containerId;
        this.data = {
            messages: [],
            uploadedFiles: 0,
            totalMessages: 0,
            ragQueries: 0
        };
        this.init();
    }

    init() {
        // Create container if it doesn't exist
        if (!document.getElementById(this.containerId)) {
            const container = document.createElement('div');
            container.id = this.containerId;
            document.body.appendChild(container);
        }

        this.width = document.getElementById(this.containerId).offsetWidth - 40;
        this.height = 300;
        this.margin = { top: 20, right: 30, bottom: 40, left: 50 };

        this.svg = d3.select(`#${this.containerId}`)
            .append('svg')
            .attr('width', this.width)
            .attr('height', this.height);

        this.createChart();
    }

    createChart() {
        const chartGroup = this.svg.append('g')
            .attr('transform', `translate(${this.margin.left},${this.margin.top})`);

        const innerWidth = this.width - this.margin.left - this.margin.right;
        const innerHeight = this.height - this.margin.top - this.margin.bottom;

        // Create axes
        this.xScale = d3.scaleTime()
            .range([0, innerWidth]);

        this.yScale = d3.scaleLinear()
            .range([innerHeight, 0]);

        this.xAxis = chartGroup.append('g')
            .attr('class', 'x-axis')
            .attr('transform', `translate(0,${innerHeight})`)
            .style('color', '#94a3b8');

        this.yAxis = chartGroup.append('g')
            .attr('class', 'y-axis')
            .style('color', '#94a3b8');

        // Create line
        this.line = d3.line()
            .x(d => this.xScale(d.time))
            .y(d => this.yScale(d.count))
            .curve(d3.curveMonotoneX);

        this.path = chartGroup.append('path')
            .attr('class', 'line')
            .style('fill', 'none')
            .style('stroke', '#6366f1')
            .style('stroke-width', 3);

        // Add gradient
        const gradient = this.svg.append('defs')
            .append('linearGradient')
            .attr('id', 'line-gradient')
            .attr('gradientUnits', 'userSpaceOnUse')
            .attr('x1', 0).attr('y1', this.yScale(0))
            .attr('x2', 0).attr('y2', this.yScale(100));

        gradient.append('stop')
            .attr('offset', '0%')
            .attr('stop-color', '#6366f1');

        gradient.append('stop')
            .attr('offset', '100%')
            .attr('stop-color', '#ec4899');

        // Create area for glow effect
        this.area = d3.area()
            .x(d => this.xScale(d.time))
            .y0(innerHeight)
            .y1(d => this.yScale(d.count))
            .curve(d3.curveMonotoneX);

        this.areaPath = chartGroup.append('path')
            .attr('class', 'area')
            .style('fill', 'url(#line-gradient)')
            .style('opacity', 0.2);

        // Add labels
        this.svg.append('text')
            .attr('class', 'chart-title')
            .attr('x', this.width / 2)
            .attr('y', 15)
            .attr('text-anchor', 'middle')
            .style('fill', '#f1f5f9')
            .style('font-size', '14px')
            .style('font-weight', '600')
            .text('Message Activity Over Time');
    }

    addMessage(isUser, useRag = false) {
        const now = new Date();
        this.data.messages.push({ time: now, isUser });
        this.data.totalMessages++;
        if (useRag && !isUser) {
            this.data.ragQueries++;
        }

        // Keep only last 20 messages for visualization
        if (this.data.messages.length > 20) {
            this.data.messages.shift();
        }

        this.updateChart();
        this.updateStats();
    }

    addFileUpload() {
        this.data.uploadedFiles++;
        this.updateStats();
    }

    updateChart() {
        // Aggregate messages by minute
        const aggregated = d3.rollup(
            this.data.messages,
            v => v.length,
            d => d3.timeMinute.floor(d.time)
        );

        const chartData = Array.from(aggregated, ([time, count]) => ({ time, count }))
            .sort((a, b) => a.time - b.time);

        if (chartData.length === 0) return;

        // Update scales
        this.xScale.domain(d3.extent(chartData, d => d.time));
        this.yScale.domain([0, d3.max(chartData, d => d.count) + 1]);

        // Update axes with transition
        this.xAxis.transition()
            .duration(500)
            .call(d3.axisBottom(this.xScale)
                .ticks(5)
                .tickFormat(d3.timeFormat('%H:%M')));

        this.yAxis.transition()
            .duration(500)
            .call(d3.axisLeft(this.yScale)
                .ticks(5));

        // Update line with transition
        this.path
            .datum(chartData)
            .transition()
            .duration(500)
            .attr('d', this.line);

        // Update area with transition
        this.areaPath
            .datum(chartData)
            .transition()
            .duration(500)
            .attr('d', this.area);
    }

    updateStats() {
        // Update stats display
        this.updateStatCard('total-messages', this.data.totalMessages);
        this.updateStatCard('uploaded-files', this.data.uploadedFiles);
        this.updateStatCard('rag-queries', this.data.ragQueries);
    }

    updateStatCard(id, value) {
        const element = document.getElementById(id);
        if (element) {
            element.textContent = value;

            // Add pulse animation
            element.style.animation = 'none';
            setTimeout(() => {
                element.style.animation = 'pulse 0.5s ease-in-out';
            }, 10);
        }
    }

    createStatsCards(container) {
        const statsHTML = `
            <div class="stats-container">
                <div class="stat-card">
                    <div class="stat-value" id="total-messages">0</div>
                    <div class="stat-label">Total Messages</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="uploaded-files">0</div>
                    <div class="stat-label">Files Uploaded</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" id="rag-queries">0</div>
                    <div class="stat-label">RAG Queries</div>
                </div>
            </div>
        `;

        const statsDiv = document.createElement('div');
        statsDiv.innerHTML = statsHTML;
        container.appendChild(statsDiv);
    }
}

// Initialize analytics when DOM is loaded
let analytics;
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        analytics = new ChatAnalytics('d3-visualization');
    });
} else {
    analytics = new ChatAnalytics('d3-visualization');
}
