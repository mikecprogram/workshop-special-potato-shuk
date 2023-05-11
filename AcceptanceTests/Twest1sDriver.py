import UseCasesProxyBridge

class TestsDriver:

    def ___init___(self):
        pass



    def getBridge(self):
        proxyBridge =  UseCasesProxyBridge()

        #unline this comment to test the implementation
        #proxyBridge.setRealBridge(Market())
        return proxyBridge

