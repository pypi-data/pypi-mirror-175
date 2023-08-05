# coding=utf-8
#####################################################
# THIS FILE IS AUTOMATICALLY GENERATED. DO NOT EDIT #
#####################################################
# noqa: E128,E201
from ...aio.asyncclient import AsyncBaseClient
from ...aio.asyncclient import createApiClient
from ...aio.asyncclient import config
from ...aio.asyncclient import createTemporaryCredentials
from ...aio.asyncclient import createSession
_defaultConfig = config


class WorkerManager(AsyncBaseClient):
    """
    This service manages workers, including provisioning for dynamic worker pools.

    Methods interacting with a provider may return a 503 response if that provider has
    not been able to start up, such as if the service to which it interfaces has an
    outage.  Such requests can be retried as for any other 5xx response.
    """

    classOptions = {
    }
    serviceName = 'worker-manager'
    apiVersion = 'v1'

    async def ping(self, *args, **kwargs):
        """
        Ping Server

        Respond without doing anything.
        This endpoint is used to check that the service is up.

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["ping"], *args, **kwargs)

    async def lbheartbeat(self, *args, **kwargs):
        """
        Load Balancer Heartbeat

        Respond without doing anything.
        This endpoint is used to check that the service is up.

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["lbheartbeat"], *args, **kwargs)

    async def version(self, *args, **kwargs):
        """
        Taskcluster Version

        Respond with the JSON version object.
        https://github.com/mozilla-services/Dockerflow/blob/main/docs/version_object.md

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["version"], *args, **kwargs)

    async def listProviders(self, *args, **kwargs):
        """
        List Providers

        Retrieve a list of providers that are available for worker pools.

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["listProviders"], *args, **kwargs)

    async def createWorkerPool(self, *args, **kwargs):
        """
        Create Worker Pool

        Create a new worker pool. If the worker pool already exists, this will throw an error.

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["createWorkerPool"], *args, **kwargs)

    async def updateWorkerPool(self, *args, **kwargs):
        """
        Update Worker Pool

        Given an existing worker pool definition, this will modify it and return
        the new definition.

        To delete a worker pool, set its `providerId` to `"null-provider"`.
        After any existing workers have exited, a cleanup job will remove the
        worker pool.  During that time, the worker pool can be updated again, such
        as to set its `providerId` to a real provider.

        This method is ``experimental``
        """

        return await self._makeApiCall(self.funcinfo["updateWorkerPool"], *args, **kwargs)

    async def deleteWorkerPool(self, *args, **kwargs):
        """
        Delete Worker Pool

        Mark a worker pool for deletion.  This is the same as updating the pool to
        set its providerId to `"null-provider"`, but does not require scope
        `worker-manager:provider:null-provider`.

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["deleteWorkerPool"], *args, **kwargs)

    async def workerPool(self, *args, **kwargs):
        """
        Get Worker Pool

        Fetch an existing worker pool defition.

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["workerPool"], *args, **kwargs)

    async def listWorkerPools(self, *args, **kwargs):
        """
        List All Worker Pools

        Get the list of all the existing worker pools.

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["listWorkerPools"], *args, **kwargs)

    async def reportWorkerError(self, *args, **kwargs):
        """
        Report an error from a worker

        Report an error that occurred on a worker.  This error will be included
        with the other errors in `listWorkerPoolErrors(workerPoolId)`.

        Workers can use this endpoint to report startup or configuration errors
        that might be associated with the worker pool configuration and thus of
        interest to a worker-pool administrator.

        NOTE: errors are publicly visible.  Ensure that none of the content
        contains secrets or other sensitive information.

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["reportWorkerError"], *args, **kwargs)

    async def listWorkerPoolErrors(self, *args, **kwargs):
        """
        List Worker Pool Errors

        Get the list of worker pool errors.

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["listWorkerPoolErrors"], *args, **kwargs)

    async def listWorkersForWorkerGroup(self, *args, **kwargs):
        """
        Workers in a specific Worker Group in a Worker Pool

        Get the list of all the existing workers in a given group in a given worker pool.

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["listWorkersForWorkerGroup"], *args, **kwargs)

    async def worker(self, *args, **kwargs):
        """
        Get a Worker

        Get a single worker.

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["worker"], *args, **kwargs)

    async def createWorker(self, *args, **kwargs):
        """
        Create a Worker

        Create a new worker.  This is only useful for worker pools where the provider
        does not create workers automatically, such as those with a `static` provider
        type.  Providers that do not support creating workers will return a 400 error.
        See the documentation for the individual providers, and in particular the
        [static provider](https://docs.taskcluster.net/docs/reference/core/worker-manager/)
        for more information.

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["createWorker"], *args, **kwargs)

    async def updateWorker(self, *args, **kwargs):
        """
        Update an existing Worker

        Update an existing worker in-place.  Like `createWorker`, this is only useful for
        worker pools where the provider does not create workers automatically.
        This method allows updating all fields in the schema unless otherwise indicated
        in the provider documentation.
        See the documentation for the individual providers, and in particular the
        [static provider](https://docs.taskcluster.net/docs/reference/core/worker-manager/)
        for more information.

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["updateWorker"], *args, **kwargs)

    async def removeWorker(self, *args, **kwargs):
        """
        Remove a Worker

        Remove an existing worker.  The precise behavior of this method depends
        on the provider implementing the given worker.  Some providers
        do not support removing workers at all, and will return a 400 error.
        Others may begin removing the worker, but it may remain available via
        the API (perhaps even in state RUNNING) afterward.

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["removeWorker"], *args, **kwargs)

    async def listWorkersForWorkerPool(self, *args, **kwargs):
        """
        Workers in a Worker Pool

        Get the list of all the existing workers in a given worker pool.

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["listWorkersForWorkerPool"], *args, **kwargs)

    async def registerWorker(self, *args, **kwargs):
        """
        Register a running worker

        Register a running worker.  Workers call this method on worker start-up.

        This call both marks the worker as running and returns the credentials
        the worker will require to perform its work.  The worker must provide
        some proof of its identity, and that proof varies by provider type.

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["registerWorker"], *args, **kwargs)

    async def reregisterWorker(self, *args, **kwargs):
        """
        Reregister a Worker

        Reregister a running worker.

        This will generate and return new Taskcluster credentials for the worker
        on that instance to use. The credentials will not live longer the
        `registrationTimeout` for that worker. The endpoint will update `terminateAfter`
        for the worker so that worker-manager does not terminate the instance.

        This method is ``experimental``
        """

        return await self._makeApiCall(self.funcinfo["reregisterWorker"], *args, **kwargs)

    async def listWorkers(self, *args, **kwargs):
        """
        Get a list of all active workers of a workerType

        Get a list of all active workers of a workerType.

        `listWorkers` allows a response to be filtered by quarantined and non quarantined workers,
        as well as the current state of the worker.
        To filter the query, you should call the end-point with one of [`quarantined`, `workerState`]
        as a query-string option with a true or false value.

        The response is paged. If this end-point returns a `continuationToken`, you
        should call the end-point again with the `continuationToken` as a query-string
        option. By default this end-point will list up to 1000 workers in a single
        page. You may limit this with the query-string parameter `limit`.

        This method is ``experimental``
        """

        return await self._makeApiCall(self.funcinfo["listWorkers"], *args, **kwargs)

    async def getWorker(self, *args, **kwargs):
        """
        Get a worker-type

        Get a worker from a worker-type.

        This method is ``experimental``
        """

        return await self._makeApiCall(self.funcinfo["getWorker"], *args, **kwargs)

    async def heartbeat(self, *args, **kwargs):
        """
        Heartbeat

        Respond with a service heartbeat.

        This endpoint is used to check on backing services this service
        depends on.

        This method is ``stable``
        """

        return await self._makeApiCall(self.funcinfo["heartbeat"], *args, **kwargs)

    funcinfo = {
        "createWorker": {
            'args': ['workerPoolId', 'workerGroup', 'workerId'],
            'input': 'v1/create-worker-request.json#',
            'method': 'put',
            'name': 'createWorker',
            'output': 'v1/worker-full.json#',
            'route': '/workers/<workerPoolId>:/<workerGroup>/<workerId>',
            'stability': 'stable',
        },
        "createWorkerPool": {
            'args': ['workerPoolId'],
            'input': 'v1/create-worker-pool-request.json#',
            'method': 'put',
            'name': 'createWorkerPool',
            'output': 'v1/worker-pool-full.json#',
            'route': '/worker-pool/<workerPoolId>',
            'stability': 'stable',
        },
        "deleteWorkerPool": {
            'args': ['workerPoolId'],
            'method': 'delete',
            'name': 'deleteWorkerPool',
            'output': 'v1/worker-pool-full.json#',
            'route': '/worker-pool/<workerPoolId>',
            'stability': 'stable',
        },
        "getWorker": {
            'args': ['provisionerId', 'workerType', 'workerGroup', 'workerId'],
            'method': 'get',
            'name': 'getWorker',
            'output': 'v1/worker-response.json#',
            'route': '/provisioners/<provisionerId>/worker-types/<workerType>/workers/<workerGroup>/<workerId>',
            'stability': 'experimental',
        },
        "heartbeat": {
            'args': [],
            'method': 'get',
            'name': 'heartbeat',
            'route': '/__heartbeat__',
            'stability': 'stable',
        },
        "lbheartbeat": {
            'args': [],
            'method': 'get',
            'name': 'lbheartbeat',
            'route': '/__lbheartbeat__',
            'stability': 'stable',
        },
        "listProviders": {
            'args': [],
            'method': 'get',
            'name': 'listProviders',
            'output': 'v1/provider-list.json#',
            'query': ['continuationToken', 'limit'],
            'route': '/providers',
            'stability': 'stable',
        },
        "listWorkerPoolErrors": {
            'args': ['workerPoolId'],
            'method': 'get',
            'name': 'listWorkerPoolErrors',
            'output': 'v1/worker-pool-error-list.json#',
            'query': ['continuationToken', 'limit'],
            'route': '/worker-pool-errors/<workerPoolId>',
            'stability': 'stable',
        },
        "listWorkerPools": {
            'args': [],
            'method': 'get',
            'name': 'listWorkerPools',
            'output': 'v1/worker-pool-list.json#',
            'query': ['continuationToken', 'limit'],
            'route': '/worker-pools',
            'stability': 'stable',
        },
        "listWorkers": {
            'args': ['provisionerId', 'workerType'],
            'method': 'get',
            'name': 'listWorkers',
            'output': 'v1/list-workers-response.json#',
            'query': ['continuationToken', 'limit', 'quarantined', 'workerState'],
            'route': '/provisioners/<provisionerId>/worker-types/<workerType>/workers',
            'stability': 'experimental',
        },
        "listWorkersForWorkerGroup": {
            'args': ['workerPoolId', 'workerGroup'],
            'method': 'get',
            'name': 'listWorkersForWorkerGroup',
            'output': 'v1/worker-list.json#',
            'query': ['continuationToken', 'limit'],
            'route': '/workers/<workerPoolId>:/<workerGroup>',
            'stability': 'stable',
        },
        "listWorkersForWorkerPool": {
            'args': ['workerPoolId'],
            'method': 'get',
            'name': 'listWorkersForWorkerPool',
            'output': 'v1/worker-list.json#',
            'query': ['continuationToken', 'limit'],
            'route': '/workers/<workerPoolId>',
            'stability': 'stable',
        },
        "ping": {
            'args': [],
            'method': 'get',
            'name': 'ping',
            'route': '/ping',
            'stability': 'stable',
        },
        "registerWorker": {
            'args': [],
            'input': 'v1/register-worker-request.json#',
            'method': 'post',
            'name': 'registerWorker',
            'output': 'v1/register-worker-response.json#',
            'route': '/worker/register',
            'stability': 'stable',
        },
        "removeWorker": {
            'args': ['workerPoolId', 'workerGroup', 'workerId'],
            'method': 'delete',
            'name': 'removeWorker',
            'route': '/workers/<workerPoolId>/<workerGroup>/<workerId>',
            'stability': 'stable',
        },
        "reportWorkerError": {
            'args': ['workerPoolId'],
            'input': 'v1/report-worker-error-request.json#',
            'method': 'post',
            'name': 'reportWorkerError',
            'output': 'v1/worker-pool-error.json#',
            'route': '/worker-pool-errors/<workerPoolId>',
            'stability': 'stable',
        },
        "reregisterWorker": {
            'args': [],
            'input': 'v1/reregister-worker-request.json#',
            'method': 'post',
            'name': 'reregisterWorker',
            'output': 'v1/reregister-worker-response.json#',
            'route': '/worker/reregister',
            'stability': 'experimental',
        },
        "updateWorker": {
            'args': ['workerPoolId', 'workerGroup', 'workerId'],
            'input': 'v1/create-worker-request.json#',
            'method': 'post',
            'name': 'updateWorker',
            'output': 'v1/worker-full.json#',
            'route': '/workers/<workerPoolId>:/<workerGroup>/<workerId>',
            'stability': 'stable',
        },
        "updateWorkerPool": {
            'args': ['workerPoolId'],
            'input': 'v1/update-worker-pool-request.json#',
            'method': 'post',
            'name': 'updateWorkerPool',
            'output': 'v1/worker-pool-full.json#',
            'route': '/worker-pool/<workerPoolId>',
            'stability': 'experimental',
        },
        "version": {
            'args': [],
            'method': 'get',
            'name': 'version',
            'route': '/__version__',
            'stability': 'stable',
        },
        "worker": {
            'args': ['workerPoolId', 'workerGroup', 'workerId'],
            'method': 'get',
            'name': 'worker',
            'output': 'v1/worker-full.json#',
            'route': '/workers/<workerPoolId>:/<workerGroup>/<workerId>',
            'stability': 'stable',
        },
        "workerPool": {
            'args': ['workerPoolId'],
            'method': 'get',
            'name': 'workerPool',
            'output': 'v1/worker-pool-full.json#',
            'route': '/worker-pool/<workerPoolId>',
            'stability': 'stable',
        },
    }


__all__ = ['createTemporaryCredentials', 'config', '_defaultConfig', 'createApiClient', 'createSession', 'WorkerManager']
