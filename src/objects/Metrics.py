import util


class Metrics:
    def __init__(self):
        self.isolated_users = []
        self.received_service = []
        self.received_service_half = []
        self.avg_distance = []
        self.isolated_systems = []

    def add_metric(self, metrics):
        self.isolated_users.append(metrics[0])

        self.received_service.append(metrics[1])

        self.received_service_half.append(metrics[2])

        self.avg_distance.append(metrics[3])

        self.isolated_systems.append(metrics[4])

    def get_metrics(self):
        return util.avg(self.isolated_users), util.avg(self.received_service), util.avg(self.received_service_half), util.avg(self.avg_distance), util.avg(self.isolated_systems)

    def get_cdf(self):
        return util.cdf(self.isolated_users), util.cdf(self.received_service), util.cdf(self.received_service_half), util.cdf(self.avg_distance), util.cdf(self.isolated_systems)

    def add_metrics_object(self, metric):
        self.isolated_users = self.isolated_users + metric.isolated_users
        self.received_service = self.received_service + metric.received_service
        self.received_service_half = self.received_service_half + metric.received_service_half
        self.avg_distance = self.avg_distance + metric.avg_distance
        self.isolated_systems = self.isolated_systems + metric.isolated_systems


    def csv_export(self):
        res = []
        for i in range(len(self.isolated_users)):
            res.append([self.isolated_users[i],self.received_service[i],self.received_service_half[i],self.avg_distance[i],self.isolated_systems[i]])

        return res

    def __str__(self):
        return "({},{},{},{},{})".format(util.avg(self.isolated_users),
                                         util.avg(self.received_service),
                                         util.avg(self.received_service_half),
                                         util.avg(self.avg_distance),
                                         util.avg(self.isolated_systems))
