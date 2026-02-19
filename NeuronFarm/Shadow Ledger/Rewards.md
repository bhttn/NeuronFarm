---
Earned: 3
Claimed: 3
---


```dataviewjs 
const data = dv.current()
let comp = data.Claimed
const remain = data.Earned - data.Claimed

const chartData = { 
	type: 'doughnut', 
	data: { 
		labels: ['UnClaimed','Claimed'], 
		datasets: [{ 
			data: [remain,comp],
			backgroundColor: [
				'rgb(232, 48, 21)',
				'rgb(27, 129, 62)',
				'rgb(255, 205, 86)'
			],
		    hoverOffset: 4
			}
			]
		} 
	}

window.renderChart(chartData, this.container); 
```
