import yaml, json

file_name = "./linux_syslog.yaml"
plugin_post_data = []
plugins = []

def read_json_file():
    with open('workload.json') as json_data:
        try:
            return(json.load(json_data))
        except:
            return {}

def read_yaml_file(filename):
    with open(filename, 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exc:
            return {}

def get_fluentd_plugins_mapping():
    return read_yaml_file(file_name)

def configure_plugin_data():
    """
    Generate plugin data based on template data as dictionary
    """
    # Read template config, merge them with plugin config and generate
    # plugin params
    x_comp_plugins = list()
    for x_plugin in logger_user_input.get('logging',{}).get('plugins', []):
        temp = dict()
        temp['source'] = {}
        temp['source']['tag'] = x_plugin.get('tags', {})
        temp['name'] = x_plugin.get('name')
        if x_plugin.get('name') in plugin_config.keys():
            plugin = plugin_config.get(x_plugin.get('name'))
            temp['source'].update(plugin.get('source'))
            if x_plugin.get('config', {}).get('log_paths'):
                temp['source']['path'] = x_plugin['config']['log_paths']
            temp['transform'] = plugin.get('transform')
            temp['parse'] = plugin.get('parse')
            temp['match'] = plugin.get('match')
        else:
            strr = 'In-Valid input plugin type.' + x_plugin.get('name')
            print(strr)
            temp['status'] = "FAILED: Unsupported logging plugin component"
            plugins.append(temp)
            continue

        temp['usr_filter'] = {}
        if x_plugin.get('config', {}).get('filters'):
            for key, value in x_plugin['config']['filters'].items():
                if isinstance(value, list):
                    temp['usr_filter'][key] = '(.*(' + '|'.join(value) + ').*?)'
                else:
                    temp['usr_filter'][key] = '(.*(' + str(value) + ').*?)'
        plugins.append(temp)
    print('Plugin data successfully Configured.')
    print('************************************')
    print plugins
    return True

def configure_plugin_file(data):
    """
    Push configured plugin data to file
    :param data: Generate plugin data based on param passed and push config to file
    :return: True if operation is successful
    """
    # Add source.
    print("Configure plugin file, data :" + str(json.dumps(data)))
    source_tag = str()
    lines = ['<source>']
    for key, val in data.get('source', {}).iteritems():
        if key == "tag":
            source_tag = data.get('name') + '.*'
            lines.append('\t' + key + ' ' + source_tag)
            continue
        lines.append('\t' + str(key) + ' ' + str(val))
    lines.append('\t' + "<parse>")
    lines.append('\t\t' + '@type none')
    lines.append('\t' + "</parse>")

    lines.append('</source>')

    # Add parser filter. if data.get('match').has_key('tag'):
    if 'tag' in data.get('match'):
        lines.append('\n<filter ' + source_tag + '.' + data.get('match').get('tag', []) + '>')
    else:
        lines.append('\n<filter ' + source_tag + '*>')
    lines.extend(['\t@type parser', '\tkey_name message', '\t<parse>'])
    for key, val in data.get('parse', {}).iteritems():
        if key == "expressions":
            for v in val:
                lines.append('\t\t' + "<pattern>")
                lines.append('\t\t\t' + 'format regexp')
                lines.append('\t\t\t' + 'expression ' + v)
                lines.append('\t\t' + "</pattern>")
            continue
        lines.append('\t\t' + key  + ' ' + val)
    lines.extend(['\t</parse>', '</filter>'])

    # Add record-transormation filter. if data.get('match').has_key('tag'):
    if 'tag' in data.get('match'):
        lines.append('\n<filter ' + source_tag + '.' + data.get('match').get('tag', []) + '>')
    else:
        lines.append('\n<filter ' + source_tag + '*>')
    lines.append('\tenable_ruby')
    lines.extend(['\t@type record_transformer', '\t<record>'])
    for key, val in data.get('transform', {}).iteritems():
        lines.append('\t\t' + key + ' \"' + val + '\"')

    for tag_key, tag_val in tags.items():
        lines.append('\t\t' + '_tag_' + str(tag_key) + ' ' + '"' + str(tag_val) + '"')
    lines.extend(['\t</record>', '</filter>'])

    # Add grep filter.
    if data.get('usr_filter', None):
        lines.append('\n<filter ' + source_tag + '*>')
        lines.append('\t@type grep')
        count = 0
        for key, value in data.get('usr_filter', {}).items():
            count = count + 1
            lines.append('\tregexp' + str(count) + ' ' + str(key) + ' ' + str(value))
        lines.append('</filter>')

    # Add match. if data.get('match').has_key('tag'):
    for x_targets in targets:
	print "***************** ----->>>"
	print x_targets
        if "status" not in x_targets:
            if 'tag' in data.get('match'):
                lines.append('\n<match ' + source_tag + '.' + data.get('match').get('tag') + '>')
                data.get('match').pop('tag')
            else:
                lines.append('\n<match ' + source_tag + '*>')

            for key, val in x_targets.iteritems():
                if key == "type":
                    key = "@" + key
                if key == "index":
                    key += "_name"
                if key == "enable":
                    continue
                lines.append('\t' + key + ' ' + val)
            lines.append('\t' + 'type_name' + ' ' + DOCUMENT)

            for key, val in data.get('match', {}).iteritems():
                lines.append('\t' + str(key) + ' ' + str(val))
            lines.append('</match>')
    conf_filename = "./" + data.get('name')
    plugin_post_data.append((conf_filename, '\n'.join(lines)))
    return True

def generate_plugins():
    """
    Generate plugin data
    :return: true if operation is successful
    """
    # Generate the files in the salt dir
    print("Generate plugins configs")
    print("************************")
    configure_plugin_data()

    for x_plugin in plugins:
        if "status" not in x_plugin:
            configure_plugin_file(x_plugin)
    return True

logger_user_input = read_json_file()
tags = logger_user_input.get('logging').get('tags')
targets = logger_user_input.get('targets')
#print("Workload : "+str(logger_user_input))
plugin_config = get_fluentd_plugins_mapping()
#print("--> plugin Config : \n"+str(plugin_config))
generate_plugins()
