'''
'Simple Tree Model Example' converted from C++/Qt 5 to Python 3/PyQt5.
Original example copyrighted from the Qt Company: http://doc.qt.io/qt-5/qtwidgets-itemviews-simpletreemodel-example.html
License is BSD as the original example.
'''


from PyQt5.QtCore    import (
   QAbstractItemModel, 
   QModelIndex, 
   Qt, 
   QVariant,
)

from PyQt5.QtWidgets import (
    QApplication, 
    QTreeView
)

class TreeItem:
    def __init__(self, data, parent=None):
        self._item_data = data
        self._parent_item = parent
        self._child_items = []

    def appendChild(self, item):
        self._child_items.append(item)

    def child(self, row):
        return self._child_items[row]

    def childCount(self):
        return len(self._child_items)

    def columnCount(self):
        return len(self._item_data)

    def data(self, column):
        if not self._item_data:
        	return QVariant()
        if column > self.columnCount():
            return QVariant()
        return QVariant(self._item_data[column])

    def parent(self):
        return self._parent_item

    def row(self):
        if self._parent_item:
            return self._parent_item._child_items.index(self)
        return 0

class TreeModel(QAbstractItemModel):
   def __init__(self, data, parent=None) :
      super().__init__(parent)
      root_data = ['Title', 'Summary']
      self._root_item = TreeItem(root_data)
      self._setupModelData(data.split('\n'), self._root_item)

   def _setupModelData(self, lines, parent):
       parents = [parent]
       indentations = [0]
       for line in lines:
           position = len(line) - len(line.lstrip(' '))
           line = line.strip()
           if not line:
               continue
           columns = [col for col in line.split('\t') if col]
           if position > indentations[-1]:
               if parents[-1].childCount() > 0:
                   parents += [ parents[-1].child(parents[-1].childCount() - 1) ]
                   indentations += [position]
           else:
               while position < indentations[-1] and len(parents) > 0:
                   parents.pop()
                   indentations.pop()
           parents[-1].appendChild(TreeItem(columns, parents[-1]))

   def rowCount(self, parent=QModelIndex()):
      if parent.column() > 0:
         return 0
      if not parent.isValid():
         parent_item = self._root_item
      else:
         parent_item = parent.internalPointer()
      return parent_item.childCount() 

   def columnCount(self, parent=QModelIndex()):
       if parent.isValid():
           return parent.internalPointer().columnCount()
       else:
           return self._root_item.columnCount()

   def data(self, index, role):
       if not index.isValid():
           return QVariant()
       item = index.internalPointer()
       if role == Qt.DisplayRole:
           return item.data(index.column())
       if role == Qt.UserRole:
           if item:
               return item._item_data
       return QVariant()

   def headerData(self, column, orientation, role=Qt.DisplayRole):
       if (orientation == Qt.Horizontal and
                role == Qt.DisplayRole):
           return self._root_item.data(column)
       return QVariant()

   def index(self, row, column, parent=QModelIndex()):
       if not self.hasIndex(row, column, parent):
          return QModelIndex()
       if not parent.isValid():
          parent_item = self._root_item
       else:
          parent_item = parent.internalPointer()
       child_item = parent_item.child(row)
       if child_item:
          return self.createIndex(row, column, child_item)
       else:
          return QModelIndex()

   def parent(self, index):
       if not index.isValid():
          return QModelIndex()
       child_item = index.internalPointer()
       if not child_item:
          return QModelIndex()
       parent_item = child_item.parent()
       if parent_item == self._root_item:
          return QModelIndex()
       return self.createIndex(parent_item.row(), 0, parent_item)


import sys

if __name__ == "__main__" :
   app = QApplication(sys.argv)
   with open('default.txt') as file:
       model = TreeModel(file.read()) 
   view  = QTreeView()
   view.setModel(model)
   view.setWindowTitle('Simple Tree Model')  # FIXIT
   view.show()
   sys.exit(app.exec_())
