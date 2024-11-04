<template>
  <div>
    <v-row>
      <v-col cols="12" md="6">
        <!-- 👉 Horizontal Form -->
        <v-card title="Horizontal Form">
          <v-card-text>
            <v-form @submit.prevent="() => {}">
              <v-row>
                <v-col cols="12">
                  <v-row no-gutters>
                    <!-- 👉 First Name -->
                    <v-col cols="12" md="3">
                      <label for="firstName">First Name</label>
                    </v-col>
                    <v-col cols="12" md="9">
                      <v-text-field id="firstName" v-model="firstName" />
                    </v-col>
                  </v-row>
                </v-col>
                <v-col cols="12">
                  <v-row no-gutters>
                    <!-- 👉 Email -->
                    <v-col cols="12" md="3">
                      <label for="email">Email</label>
                    </v-col>
                    <v-col cols="12" md="9">
                      <v-text-field id="email" v-model="email" placeholder="johndoe@email.com" persistent-placeholder />
                    </v-col>
                  </v-row>
                </v-col>
                <v-col cols="12">
                  <v-row no-gutters>
                    <!-- 👉 Mobile -->
                    <v-col cols="12" md="3">
                      <label for="mobile">Mobile</label>
                    </v-col>
                    <v-col cols="12" md="9">
                      <v-text-field id="mobile" v-model="mobile" type="number" placeholder="+1 123 456 7890" persistent-placeholder />
                    </v-col>
                  </v-row>
                </v-col>
                <v-col cols="12">
                  <v-row no-gutters>
                    <!-- 👉 Password -->
                    <v-col cols="12" md="3">
                      <label for="password">Password</label>
                    </v-col>
                    <v-col cols="12" md="9">
                      <v-text-field
                        id="password"
                        v-model="password"
                        autocomplete="on"
                        type="password"
                        placeholder="············"
                        persistent-placeholder
                      />
                    </v-col>
                  </v-row>
                </v-col>

                <!-- 👉 Remember me -->
                <v-col offset-md="3" cols="12" md="9">
                  <v-checkbox v-model="checkbox" label="Remember me" />
                </v-col>

                <!-- 👉 submit and reset button -->
                <v-col offset-md="3" cols="12" md="9" class="d-flex gap-4">
                  <v-btn type="submit"> Submit </v-btn>
                  <v-btn color="secondary" variant="outlined" type="reset"> Reset </v-btn>
                </v-col>
              </v-row>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <!-- 👉 Horizontal Form with Icons -->
        <v-card title="Horizontal Form with Icons">
          <v-card-text>
            <v-form @submit.prevent="() => {}">
              <v-row>
                <!-- 👉 First Name -->
                <v-col cols="12">
                  <v-row no-gutters>
                    <v-col cols="12" md="3">
                      <label for="firstNameHorizontalIcons">First Name</label>
                    </v-col>
                    <v-col cols="12" md="9">
                      <v-text-field
                        id="firstNameHorizontalIcons"
                        v-model="firstName"
                        prepend-inner-icon="ri-user-line"
                        placeholder="John"
                        persistent-placeholder
                      />
                    </v-col>
                  </v-row>
                </v-col>

                <!-- 👉 Email -->
                <v-col cols="12">
                  <v-row no-gutters>
                    <v-col cols="12" md="3">
                      <label for="emailHorizontalIcons">Email</label>
                    </v-col>
                    <v-col cols="12" md="9">
                      <v-text-field
                        id="emailHorizontalIcons"
                        v-model="email"
                        prepend-inner-icon="ri-mail-line"
                        placeholder="johndoe@email.com"
                        persistent-placeholder
                      />
                    </v-col>
                  </v-row>
                </v-col>

                <!-- 👉 Mobile -->
                <v-col cols="12">
                  <v-row no-gutters>
                    <v-col cols="12" md="3">
                      <label for="mobileHorizontalIcons">Mobile</label>
                    </v-col>
                    <v-col cols="12" md="9">
                      <v-text-field
                        id="mobileHorizontalIcons"
                        v-model="mobile"
                        type="number"
                        prepend-inner-icon="ri-smartphone-line"
                        placeholder="+1 123 456 7890"
                        persistent-placeholder
                      />
                    </v-col>
                  </v-row>
                </v-col>

                <!-- 👉 Password -->
                <v-col cols="12">
                  <v-row no-gutters>
                    <v-col cols="12" md="3">
                      <label for="passwordHorizontalIcons">Password</label>
                    </v-col>
                    <v-col cols="12" md="9">
                      <v-text-field
                        id="passwordHorizontalIcons"
                        v-model="password"
                        prepend-inner-icon="ri-lock-line"
                        autocomplete="on"
                        type="password"
                        placeholder="············"
                        persistent-placeholder
                      />
                    </v-col>
                  </v-row>
                </v-col>

                <!-- 👉 Checkbox -->
                <v-col offset-md="3" cols="12" md="9">
                  <v-checkbox v-model="checkbox" label="Remember me" />
                </v-col>

                <!-- 👉 submit and reset button -->
                <v-col offset-md="3" cols="12" md="9" class="d-flex gap-4">
                  <v-btn type="submit"> Submit </v-btn>
                  <v-btn color="secondary" type="reset" variant="outlined"> Reset </v-btn>
                </v-col>
              </v-row>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <!-- 👉 Vertical Form -->
        <v-card title="Vertical Form">
          <v-card-text>
            <v-form @submit.prevent="() => {}">
              <v-row>
                <v-col cols="12">
                  <v-text-field v-model="firstName" label="First Name" placeholder="John" />
                </v-col>
                <v-col cols="12">
                  <v-text-field v-model="email" label="Email" type="email" placeholder="johndoe@example.com" />
                </v-col>
                <v-col cols="12">
                  <v-text-field v-model="mobile" label="Mobile" placeholder="+1 123 456 7890" type="number" />
                </v-col>
                <v-col cols="12">
                  <v-text-field v-model="password" label="Password" autocomplete="on" type="password" placeholder="············" />
                </v-col>
                <v-col cols="12">
                  <v-checkbox v-model="checkbox" label="Remember me" />
                </v-col>
                <v-col cols="12" class="d-flex gap-4">
                  <v-btn type="submit"> Submit </v-btn>
                  <v-btn type="reset" color="secondary" variant="outlined"> Reset </v-btn>
                </v-col>
              </v-row>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <!-- 👉 Vertical Form with Icons -->
        <v-card title="Vertical Form with Icons">
          <v-card-text>
            <v-form @submit.prevent>
              <v-row>
                <v-col cols="12">
                  <v-text-field v-model="firstName" prepend-inner-icon="ri-user-line" label="First Name" placeholder="John" />
                </v-col>
                <v-col cols="12">
                  <v-text-field v-model="email" prepend-inner-icon="ri-mail-line" label="Email" type="email" placeholder="johndoe@example.com" />
                </v-col>
                <v-col cols="12">
                  <v-text-field v-model="mobile" prepend-inner-icon="ri-smartphone-line" label="Mobile" placeholder="+1 123 456 7890" type="number" />
                </v-col>
                <v-col cols="12">
                  <v-text-field
                    v-model="password"
                    prepend-inner-icon="ri-lock-line"
                    label="Password"
                    autocomplete="on"
                    type="password"
                    placeholder="············"
                  />
                </v-col>
                <v-col cols="12">
                  <v-checkbox v-model="checkbox" label="Remember me" />
                </v-col>
                <v-col cols="12">
                  <v-btn type="submit" class="me-2"> Submit </v-btn>
                  <v-btn color="secondary" type="reset" variant="outlined"> Reset </v-btn>
                </v-col>
              </v-row>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12">
        <!-- 👉 Multiple Column -->
        <v-card title="Multiple Column">
          <v-card-text>
            <v-form @submit.prevent="() => {}">
              <v-row>
                <!-- 👉 First Name -->
                <v-col cols="12" md="6">
                  <v-text-field v-model="firstName" label="First Name" placeholder="John" />
                </v-col>
                <!-- 👉 Last Name -->
                <v-col cols="12" md="6">
                  <v-text-field v-model="lastName" label="Last Name" placeholder="Doe" />
                </v-col>
                <!-- 👉 Email -->
                <v-col cols="12" md="6">
                  <v-text-field v-model="email" label="Email" placeholder="johndoe@email.com" />
                </v-col>
                <!-- 👉 City -->
                <v-col cols="12" md="6">
                  <v-text-field v-model="city" label="City" placeholder="New York" />
                </v-col>
                <!-- 👉 Country -->
                <v-col cols="12" md="6">
                  <v-text-field v-model="country" label="Country" placeholder="United States" />
                </v-col>
                <!-- 👉 Company -->
                <v-col cols="12" md="6">
                  <v-text-field v-model="company" label="Company" placeholder="Pixinvent" />
                </v-col>
                <!-- 👉 Remember me -->
                <v-col cols="12">
                  <v-checkbox v-model="checkbox" label="Remember me" />
                </v-col>
                <v-col cols="12" class="d-flex gap-4">
                  <v-btn type="submit"> Submit </v-btn>
                  <v-btn type="reset" color="secondary" variant="outlined"> Reset </v-btn>
                </v-col>
              </v-row>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup lang="ts">
const firstName = ref('');
const lastName = ref('');
const city = ref('');
const country = ref('');
const company = ref('');
const email = ref('');
const mobile = ref<number>();
const password = ref<string>();
const checkbox = ref(false);
</script>
