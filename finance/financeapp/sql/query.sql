select cashin as cashflow, fc.description, "date", fc3."name" as category, fc5."name" as contractor, 'cashin' as "type"
from financeapp_cashin fc
left join financeapp_cashincategories fc3 on fc.cashin_category_id = fc3.id
left join financeapp_contractor fc5 on fc5.id = fc.contractor_id
where user_id = %s
and transacted = true
and "date" BETWEEN %s AND %s
union
select cashout as cashflow, fc2.description, "date", fc4."name" as category, fc5."name" as contractor, 'cashout' as "type"
from financeapp_cashout fc2
left join financeapp_cashoutcategories fc4 on fc4.id = fc2.cashout_category_id
left join financeapp_contractor fc5 on fc5.id = fc2.contractor_id
where user_id = %s
and transacted = true
and "date" BETWEEN %s AND %s
order by "date" desc