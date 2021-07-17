select cot_subscriber.customerid, datetime(cot_subscriber.timestamp, 'localtime'), cot_subscriber_alias.alias
from cot_subscriber left join cot_subscriber_alias
on cot_subscriber.customerid = cot_subscriber_alias.customerid
   and cot_subscriber.subscriber = cot_subscriber_alias.subscriber
union all
select cot_subscriber.customerid, datetime(cot_subscriber.timestamp, 'localtime'), cot_subscriber_alias.alias
from cot_subscriber left join cot_subscriber_alias
on cot_subscriber.customerid = cot_subscriber_alias.customerid
   and cot_subscriber.subscriber = cot_subscriber_alias.subscriber
where cot_subscriber_alias.customerid is null;


   
