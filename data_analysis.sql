-- ================================================
-- Sales Data Analysis
-- Database: company | Table: df_orders
-- ================================================

USE company;

# Total sales and profit by caregory 
select 
	category,
	round(sum(sale_price), 2) as total_sales,
	round(sum(profit), 2) as total_profit,
    round((sum(profit)/sum(sale_price))*100, 2) as profit_margin_pct
from df_orders
group by category
order by total_sales desc;

# Top 10 most profitable states
select
	state,
    round(sum(sale_price), 2) as total_sales,
    round(sum(profit), 2) as total_profit
from df_orders
group by state
order by total_profit desc;

# Monthly revenue trend
select
    DATE_FORMAT(order_date, '%Y-%m') AS month,
    ROUND(SUM(sale_price), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit
from df_orders
group by month
order by month;

# Loss making orders
select 
    order_id,
    category,
    sub_category,
    state,
    sale_price,
    profit
from df_orders
where profit < 0
order by profit ASC;

# Best performing sub category
select
    sub_category,
    COUNT(*) AS total_orders,
    ROUND(SUM(sale_price), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit
from df_orders
group by sub_category
order by total_profit DESC;

# Sales by region and segment
select
    region,
    segment,
    ROUND(SUM(sale_price), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit
from df_orders
group by region, segment
order by region, total_sales DESC;