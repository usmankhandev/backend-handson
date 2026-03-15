const http = require('http');
const {ApolloServer} = require('@apollo/server');
const {startStandaloneServer} = require('@apollo/server/standalone');
const typeDefs = require('./graphql/schema');
const resolvers = require('./graphql/resolver');

async function startServer() {

    const server = new ApolloServer({
        typeDefs,
        resolvers,
    })

    const {url} = await startStandaloneServer(server, {
        listen: {port: 4000}
    })
    console.log(`Server is running at ${url}`);
}

startServer();