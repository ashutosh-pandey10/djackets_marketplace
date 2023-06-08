<template>
    <div class="page-checkout">
        <div class="columns is-multiline">
            <div class="column is-12">
                <h1 class="title">Checkout</h1>
            </div>

            <div class="column is-12 box">
                <table class="table is-fullwidth">
                    <thead>
                        <tr>
                            <th>Product</th>
                            <th>Price</th>
                            <th>Quantity</th>
                            <th>Total</th>
                        </tr>
                    </thead>

                    <tbody>
                        <tr
                            v-for="item in cart.items"
                            v-bind:key="item.product.id"
                        >
                            <td>{{ item.product.name }}</td>
                            <td>₹{{ item.product.price }}</td>
                            <td>{{ item.quantity }}</td>
                            <td>₹{{ getItemTotal(item).toFixed(2) }}</td>
                        </tr>
                    </tbody>

                    <tfoot>
                        <tr>
                            <td colspan="2">Total</td>
                            <td>{{ cartTotalLength }}</td>
                            <td>₹{{ cartTotalPrice.toFixed(2) }}</td>
                        </tr>
                    </tfoot>
                </table>
            </div>

            <div class="column is-12 box">
                <h2 class="subtitle">Shipping details</h2>

                <p class="has-text-grey mb-4">* All fields are required</p>

                <div class="columns is-multiline">
                    <div class="column is-6">
                        <div class="field">
                            <label>First name*</label>
                            <div class="control">
                                <input type="text" class="input" v-model="first_name">
                            </div>
                        </div>

                        <div class="field">
                            <label>Last name*</label>
                            <div class="control">
                                <input type="text" class="input" v-model="last_name">
                            </div>
                        </div>

                        <div class="field">
                            <label>E-mail*</label>
                            <div class="control">
                                <input type="email" class="input" v-model="email">
                            </div>
                        </div>

                        <div class="field">
                            <label>Phone*</label>
                            <div class="control">
                                <input type="text" class="input" v-model="phone">
                            </div>
                        </div>
                    </div>

                    <div class="column is-6">
                        <div class="field">
                            <label>Address*</label>
                            <div class="control">
                                <input type="text" class="input" v-model="address">
                            </div>
                        </div>

                        <div class="field">
                            <label>Zip code*</label>
                            <div class="control">
                                <input type="text" class="input" v-model="zipcode">
                            </div>
                        </div>

                        <div class="field">
                            <label>Place*</label>
                            <div class="control">
                                <input type="text" class="input" v-model="place">
                            </div>
                        </div>
                    </div>
                </div>

                <div class="notification is-danger mt-4" v-if="errors.length">
                    <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                </div>

                <hr>


                <template v-if="cartTotalLength">
                    <hr>

                    <button class="button is-dark" @click="submitForm">Pay with Razorpay</button>
                </template>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    name: 'Checkout',
    data() {
        return {
            cart: {
                items: []
            },
            order_id: '',
            first_name: '',
            last_name: '',
            email: '',
            phone: '',
            address: '',
            zipcode: '',
            place: '',
            errors: []
        }
    },
    mounted() {
        document.title = 'Checkout | Djackets'

        this.cart = this.$store.state.cart
    },
    methods: {
        getItemTotal(item) {
            return item.quantity * item.product.price
        },
        submitForm() {
            this.errors = []

            if (this.first_name === '') {
                this.errors.push('The first name field is missing!')
            }

            if (this.last_name === '') {
                this.errors.push('The last name field is missing!')
            }

            if (this.email === '') {
                this.errors.push('The email field is missing!')
            }

            if (this.phone === '') {
                this.errors.push('The phone field is missing!')
            }

            if (this.address === '') {
                this.errors.push('The address field is missing!')
            }

            if (this.zipcode === '') {
                this.errors.push('The zip code field is missing!')
            }

            if (this.place === '') {
                this.errors.push('The place field is missing!')
            }

            if (!this.errors.length) {
                this.$store.commit('setIsLoading', true)


                this.razorpay_handler()
            }
        },
        async razorpay_handler() {
            const items = []

            for (const element of this.cart.items) {
                const item = element
                const obj = {
                    product: item.product.id,
                    quantity: item.quantity,
                    price: item.product.price * item.quantity
                }

                items.push(obj)
            }

            const data = {
                'first_name': this.first_name,
                'order_id' : this.order_id,
                'last_name': this.last_name,
                'email': this.email,
                'address': this.address,
                'zipcode': this.zipcode,
                'place': this.place,
                'phone': this.phone,
                'items': items
                
            }

            await axios
                .post('/api/v1/checkout/', data)
                .then(response => {    
                    
                    let responseData = response.data 
                    console.log("got respone from checkout end point.")
                    console.log(responseData)
                    let options = {
                        key: "rzp_test_sMaBGTDZ8szQZG",
                        key_secret:"LAip9602czN9MlqUVi6BpvQb",
                        amount: responseData.paid_amount,
                        order_id: responseData.order_id,
                        currency:"INR",
                        name:"Djackets receipt",
                        description:"for testing purpose",

                        handler: function(res){
                            // Put up a function over here to verify payment by not using Django
                            fetch('/api/v1/validate_payment/', {
                                        method: 'POST',
                                        headers: {
                                            'Content-Type': 'application/json',
                                            'X-CSRFToken': '{{ csrf_token }}'
                                        },
                                        credentials: 'same-origin',
                                        body: JSON.stringify({
                                            'razorpay_payment_id': res.razorpay_payment_id,
                                            'razorpay_order_id': res.razorpay_order_id,
                                            'razorpay_signature': res.razorpay_signature
                                        })
                                    })
                                    .then(function(response) {
                                        return response.json();
                                    })
                                    .catch(error => {
                                        this.errors.push('Something went wrong. Please try again. Line 249')

                                        console.log(error)
                                    })
                            
                        },
                        prefill: {
                        name: responseData.first_name + " " + responseData.last_name,
                        email: responseData.email,
                        contact: responseData.phone
                        },
                        notes:{
                        address: responseData.address
                        },
                        theme: {
                        color:"#3399cc"
                        }
                    };

                    console.log("Everything fine till razorpay object creation")
                    
                    let rzp = new Razorpay(options)
                    rzp.open()
                    // Need to fill in the options variable whiich will inturn open the razorpay prompt
                    // entering the details will return a payment_id, which can then be used to retrieve payment details 
                    this.$store.commit('clearCart')
                    this.$router.push('/cart/success')
                }
   
                )                
                .catch(error => {
                    this.errors.push('Something went wrong. Please try again. Line 249')

                    console.log(error)
                })
            
            
            
            this.$store.commit('setIsLoading', false)
            
            
            
            
        }
    },
    computed: {
        cartTotalPrice() {
            return this.cart.items.reduce((acc, curVal) => {
                return acc += curVal.product.price * curVal.quantity
            }, 0)
        },
        cartTotalLength() {
            return this.cart.items.reduce((acc, curVal) => {
                return acc += curVal.quantity
            }, 0)
        }
    }
}
</script>