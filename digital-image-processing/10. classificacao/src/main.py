from Utils import Data
import DecisionTree as dt

def main():

    ### PDI ~ C4.5
    # train_x, train_y, test_x, test_y = Data().fetchFromH5('train_catvnoncat.h5', 'test_catvnoncat.h5')
    # criterion = "entropy"

    # training_data = dt.preProcess(train_x, train_y, normalize=True, gray=True)
    # decision_tree = dt.growTree(training_data, criterion)

    # dt.plotDiagram(decision_tree, extension=criterion)
    # dt.prune(decision_tree, criterion, 0.75)
    # dt.plotDiagram(decision_tree, extension=(criterion+"_pruned"))

    # test_data = dt.preProcess(test_x, normalize=True, gray=True)
    # result_text = dt.classify(decision_tree, test_data, test_y)
    # print("\n%s" % "\n".join(result_text))
    # Data().saveVariable(name="decision_tree", extension=(criterion+"_classify_result"), value=result_text)

    ### CI ~ C4.5
    train_x, train_y = Data().fetchFromPath('characters', 't0')
    test_x, test_y = Data().fetchFromPath('characters', 't1')
    criterion = "entropy"

    training_data = dt.preProcess(train_x, train_y, norm=True, gray=True, seg=True)
    decision_tree = dt.growTree(training_data, criterion)

    dt.plotDiagram(decision_tree, extension=criterion)
    # dt.prune(decision_tree, criterion, 0.5)
    # dt.plotDiagram(decision_tree, extension=(criterion+"_pruned"))

    test_data = dt.preProcess(test_x, norm=True, gray=True, seg=True)
    result_text = dt.classify(decision_tree, test_data, test_y)
    Data().saveVariable(name="decision_tree", extension=(criterion+"_classify_result"), value=result_text)
    print("\n%s" % "\n".join(result_text))

    ## CI ~ CART
    # cart = dt.CART()
    # train_x, train_y = Data().fetchFromPath('characters', 't0')
    # test_x, test_y = Data().fetchFromPath('characters', 't1')

    # training_data = dt.preProcess(train_x, train_y, norm=True, gray=True, seg=True)
    # testing_data = dt.preProcess(test_x, test_y, norm=True, gray=True, seg=True)
    # attr_names = ['i1','i2','i3','i4','i5','i6','i7']
    
    # cart.load(training_data, train_y, attr_names, testing_data)
    # cart.train()
    # cart.predict()
    # cart.render(extension="CART")

if __name__ == '__main__':
    main()