from pprint import pprint

from collectors.disk import collect_disk_metrics

pprint(collect_disk_metrics())