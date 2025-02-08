from RedBlackTree import RedBlackTree

if __name__ == "__main__":
    bst = RedBlackTree()

    # Questão 6 - Operações
    keys_to_insert = [5, 16, 22, 45, 2, 10, 18, 30, 50, 12, 1]
    for key in keys_to_insert:
        bst.insert(key)

    print("Árvore em ordem de inserção:")
    bst.printInOrder()
    print("\nÁrvore após inserções:")
    bst.printTree()

    print("\nProcurando pelas chaves 22 e 15:")
    print(bst.find(22).data if bst.find(22) != bst.TNULL else "Não encontrado")
    print(bst.find(15).data if bst.find(15) != bst.TNULL else "Não encontrado")

    keys_to_delete = [30, 10, 22]
    for key in keys_to_delete:
        bst.deleteByVal(key)
    print("\nÁrvore após exclusões:")
    bst.printTree()
    keys_to_insert = [25, 9, 33, 50]
    for key in keys_to_insert:
        bst.insert(key)  
    print("\nÁrvore novas inserções:")
    bst.printTree()

    print("\nMaior valor:", bst.findMax())
    print("Menor valor:", bst.findMin())
    print("Quinto menor valor:", bst.findKth(5))

    print("\nElementos entre 10 e 30:")
    bst.findInterval(10, 30)