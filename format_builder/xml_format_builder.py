# Build the xml format according to tags and recommended tags file and inv_vocabulary

from xml.dom.minidom import Document

def build_xml_format(name_object, tags, recommended_tags, gauge_metric):
	doc_xml = Document()
	lastfm_object = doc_xml.createElement("metrics")
	doc_xml.appendChild(lastfm_object)
	name = doc_xml.createElement("name")
	name_str = doc_xml.createTextNode("lastfm.artist." + name_object)
	name.appendChild(name_str)
	lastfm_object.appendChild(name)
	gauge_node = doc_xml.createElement("gauge_metric")
	gauge_value = doc_xml.createTextNode(str(gauge_metric))
	gauge_node.appendChild(gauge_value)
	lastfm_object.appendChild(gauge_node)
	tags_node = doc_xml.createElement("tags")
	for tag in tags:
		item = doc_xml.createElement("item")
		item_str = doc_xml.createTextNode(tag[0]+ "--#" + str(tag[1]))
		item.appendChild(item_str)
		tags_node.appendChild(item)
	lastfm_object.appendChild(tags_node)
	recommended_tags_node = doc_xml.createElement("recommended_tags")
	for tag in recommended_tags:
		item = doc_xml.createElement("item")
		item_str = doc_xml.createTextNode(tag[0]+ "--#" + str(tag[1]))
		item.appendChild(item_str)
		recommended_tags_node.appendChild(item)
	lastfm_object.appendChild(recommended_tags_node)
	doc_xml.appendChild(lastfm_object)
	return doc_xml
