---
Goal: 10
StartDate: 2024-09-21
---


```dataviewjs 
const data = dv.current()
let pages = dv.pages('"Shadow Ledger"').where(t => t.Date > data.StartDate).where(s => s.Strength);

let comp = pages.Strength.length;
const remain = data.goal - comp

const chartData = { 
	type: 'doughnut', 
	data: { 
		labels: ['Remaining','Completed'], 
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


### Table
```dataviewjs
let pages = dv.pages('"Shadow Ledger"').where(s => s.Strength);

let results = pages.map((page, index) => [
	page.file.link, 
	page.Strength,
	]);

dv.table(["Date", "Result"], results);
//dv.paragraph(pages.map(p => p.file.name).values);
//dv.paragraph(dv.func.default(dv.func.sum(pages.Strength), 0))
//dv.paragraph(pages.Strength.length)
```