def reconnect(pipes, connectors, tolerance):
    pipeConnectors = []
    connectorC = []
    for i in pipes:
        ppConnectors = i.ConnectorManager.Connectors
        for pp in ppConnectors:
            pipeConnectors.append(pp)
            # print(pp)
    for connectorSets in connectors:
        cs = connectorSets.MEPModel.ConnectorManager.Connectors
        for a in cs:
            connectorC.append(a)
            # print(a)
    for ca in pipeConnectors:
        pipeLoc = ca.Origin
        for cc in connectorC:
            connectorLoc = cc.Origin
            if pipeLoc.DistanceTo(connectorLoc) < tolerance:
                try:
                    ca.ConnectTo(cc)

                except:
                    pass