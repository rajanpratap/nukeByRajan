import constants as as _constants

def wire_in(path, source_node, nuke):
  """Method to paste nuke script of a read node(the one from which it is created) to a current nuke session replacing that read node.
  Args:
    path(str): A nuke script path to import in current nuke session.
    source_node(nuke.Node): nuke source read node object of which nuke script is being pasted.
    nuke(nuke.instance): A nuke Instance(import nuke).
  """
    
  #when read node is not connected to any node.
  try:
    terminal_node = source_node.dependent()[0]
  except IndexError:
    try:
      terminal_node = source_node.dependent()[0]
    except IndexError:
      nuke.nodePaste(path)
      return False
  nuke.nodePaste(path)
  pasted_nodes = nuke.SelectedNodes()
  write_node = None

  #grab the first matching write we find - if none, fallback to the first write node in script
  for node in pasted_nodes:
    if node.Class() not in ("DeepWrite" ,"Write"):
      continue
    elif node["file"].value() == source_node["file"].value():
      write_node = node
      break
    elif not write_node:
      write_node = node
  
  des_x, dest_y = source_node.xpos(), source_node.ypos() -source_node.screenHeight() - 2 * _constants.NODE_GAP - _constants.WRITE_NODE_SCREENHEIGHT
  offset_x, offset_y = dest_x - write_node.xpos(), dest_y - write_node.ypos()
  #offset all pasted nodes accordingly
  for pnode in pasted_nodes:
    pnode.setXYpos(pnode.xpos()+offset_x, pnode.ypos()+offset_y)
  
  #create a NoOp node within appropriate group, just below source Node(all connections are auto preserved)
  deselect_all()
  input_node = nuke.createNode("NoOp")
  input_node["label"].setValue("{0} render script".format(node.fullName()))
  newp = wnode.xpos(), wnode.ypos()
  input_node.setXYpos(newp[0], newp[1])
  input_node.setXYpos(write_node.xpos() + 150)
  sorce_node.setXYpos(source_node.xpos() + 150, source_node.ypos() - source_node.screenHeight() - _constant.NODE_GAP)
  _dag_select.deselectall()
  for node in pasted_nodes:
    node.setSelected(True)
  
  input_node.setInput(0, write_node.input(0)
  terminal_node.setInput(0, input_node)

def deselectall(nuke):
  for node in nuke.allNodes():
    node.setSelected(False)
  
