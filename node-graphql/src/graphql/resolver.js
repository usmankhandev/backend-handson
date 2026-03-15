const products = require('../data/product');

const resolvers = {
    Query: {
        products: () => products,
        product: (_, {id}) =>  products.find((product) => product.id === parseInt(id))
    },

    Mutation: {
        createProduct: (_, {name, category, price, inStock}) => {
            const newProduct = {
                id: products.length + 1,
                name,
                category,
                price,
                inStock
            }
            products.push(newProduct);
            return newProduct;  
        },
        deleteProduct: (_, {id}) => {
            const index = products.findIndex((product) =>  product.id === parseInt(id));
            if(index === -1) return;
            products.splice(index, 1);
            return true;
        },

        updateProduct: (_, {id, name, category, price, inStock}) => {
            const product = products.find((product) => product.id === parseInt(id));
            if(!product) return;
            if(name !== undefined) product.name = name;
            if(category !== undefined) product.category = category;
            if(price !== undefined) product.price = price;
            if(inStock !== undefined) product.inStock = inStock;
            return product;
        }
    }
}


module.exports = resolvers;