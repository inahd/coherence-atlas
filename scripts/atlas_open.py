import sys

TARGET = (sys.argv[1] if len(sys.argv)>1 else 'rohini').strip().lower()

paths = {
  'dashboard': '/opt/atlas/memory/reports/dashboard.html',
  'graph': '/opt/atlas/memory/graphs/resolved_graph_interactive.html',
  'rohini_report': '/opt/atlas/memory/reports/cluster_nakshatra_rohini.md',
  'rohini_page': '/opt/atlas/docs/wiki_entities/nakshatra__rohini.md',
  'north_star': '/opt/atlas/docs/north_star_demo.md',
  'vision': '/opt/atlas/docs/vision.md',
}

if TARGET in ('rohini','demo'): 
  print('[OPEN PATHS]')
  print('North Star demo:', paths['north_star'])
  print('Dashboard:', paths['dashboard'])
  print('Interactive graph:', paths['graph'])
  print('Rohini report:', paths['rohini_report'])
  print('Rohini page:', paths['rohini_page'])
elif TARGET in paths:
  print(paths[TARGET])
else:
  print('Usage: atlas open rohini|dashboard|graph|rohini_report|rohini_page|north_star|vision')

