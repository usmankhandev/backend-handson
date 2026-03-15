// The file will tell the structure of the data and how to query it
// It will define the types and the queries and mutations

const {gql} = require('graphql-tag');


// String
// Int
// Float
// Boolean
// ID -> unique identifier


const typeDefs = gql `

type Product {

    id: ID!
    name: String!
    category: String!
    price: Float!
    inStock: Boolean!
}

type Query {
    products: [Product!]!
    product(id: ID!): Product
}
    

type Mutation {
createProduct(name: String!, category: String!, price: Float!, inStock: Boolean!): Product!
deleteProduct(id: ID!): Boolean!
updateProduct(id: ID!, name: String, category: String, price: Float, inStock: Boolean): Product!

}
`


module.exports = typeDefs