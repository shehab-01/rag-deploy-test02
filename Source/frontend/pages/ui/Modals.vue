<template>
  <v-row>
    <v-col cols="12">
      <v-row>
        <!-- Examples -->
        <v-col cols="12">
          <UiChildCard title="Modal Examples">
            <h2>
              <a href="https://vuetifyjs.com/en/components/dialogs/#usage" target="_blank">Document</a>
            </h2>
            <div>
              <v-btn variant="outlined" prepend-icon="" class="ma-5" @click="data.dialog1 = true">Ex: Default</v-btn>
              <v-btn variant="outlined" prepend-icon="" class="ma-5" @click="data.dialog2 = true">Ex: Persistent</v-btn>
              <v-btn variant="outlined" prepend-icon="mdi-earth" class="ma-5" @click="data.dialog3 = true">Ex: Scrollable</v-btn>
              <v-btn variant="outlined" prepend-icon="mdi-account" class="ma-5" @click="data.dialog4 = true">Ex: Form</v-btn>
            </div>
          </UiChildCard>
        </v-col>
        <!-- Messages -->
        <v-col cols="12">
          <UiChildCard title="Modal Messages">
            <div>
              <v-btn variant="outlined" prepend-icon="" class="ma-5" @click="page.btnAlert1">Message: Alert1</v-btn>
              <v-btn variant="outlined" prepend-icon="" class="ma-5" @click="page.btnAlert2">Message: Alert2</v-btn>
              <v-btn variant="outlined" prepend-icon="" class="ma-5" @click="page.btnConfirm">Message: Confirm</v-btn>
              <v-btn variant="outlined" prepend-icon="" class="ma-5" @click="page.btnValid">Message: Valid</v-btn>
              <v-btn variant="outlined" prepend-icon="" class="ma-5" @click="page.btnError">Message: Error</v-btn>
            </div>
          </UiChildCard>
        </v-col>
        <!--  -->
        <v-col cols="12" v-if="false">
          <UiChildCard title="">
            <div></div>
          </UiChildCard>
        </v-col>
      </v-row>
    </v-col>
  </v-row>

  <template>
    <!-- Default -->
    <v-dialog v-model="data.dialog1" width="auto">
      <v-card
        max-width="400"
        prepend-icon="mdi-update"
        text="Your application will relaunch automatically after the update is complete."
        title="Update in progress"
      >
        <template v-slot:actions>
          <v-btn class="ms-auto" text="Ok" @click="data.dialog1 = false"></v-btn>
        </template>
      </v-card>
    </v-dialog>

    <!-- Persistent -->
    <v-dialog v-model="data.dialog2" max-width="400" persistent>
      <v-card
        prepend-icon="mdi-map-marker"
        text="Let Google help apps determine location. This means sending anonymous location data to Google, even when no apps are running."
        title="Use Google's location service?"
      >
        <template v-slot:actions>
          <v-spacer></v-spacer>
          <v-btn @click="data.dialog2 = false"> Disagree </v-btn>
          <v-btn @click="data.dialog2 = false"> Agree </v-btn>
        </template>
      </v-card>
    </v-dialog>

    <!-- Scrollable -->
    <v-dialog v-model="data.dialog3" width="auto" scrollable>
      <template v-slot:default="{ isActive }">
        <v-card prepend-icon="mdi-earth" title="Select Country">
          <v-divider class="mt-0"></v-divider>
          <v-card-text class="px-4" style="height: 300px">
            <v-radio-group messages="Select a Country from the radio group" column>
              <v-radio label="Bahamas, The" value="bahamas"></v-radio>
              <v-radio label="Bahrain" value="bahrain"></v-radio>
              <v-radio label="Bangladesh" value="bangladesh"></v-radio>
              <v-radio label="Barbados" value="barbados"></v-radio>
              <v-radio label="Belarus" value="belarus"></v-radio>
              <v-radio label="Belgium" value="belgium"></v-radio>
              <v-radio label="Belize" value="belize"></v-radio>
              <v-radio label="Benin" value="benin"></v-radio>
              <v-radio label="Bhutan" value="bhutan"></v-radio>
              <v-radio label="Bolivia" value="bolivia"></v-radio>
              <v-radio label="Bosnia and Herzegovina" value="bosnia"></v-radio>
              <v-radio label="Botswana" value="botswana"></v-radio>
              <v-radio label="Brazil" value="brazil"></v-radio>
              <v-radio label="Brunei" value="brunei"></v-radio>
              <v-radio label="Bulgaria" value="bulgaria"></v-radio>
              <v-radio label="Burkina Faso" value="burkina"></v-radio>
              <v-radio label="Burma" value="burma"></v-radio>
              <v-radio label="Burundi" value="burundi"></v-radio>
            </v-radio-group>
          </v-card-text>
          <v-divider></v-divider>
          <v-card-actions>
            <v-btn text="Close" @click="isActive.value = false"></v-btn>
            <v-btn text="Save" @click="isActive.value = false"></v-btn>
          </v-card-actions>
        </v-card>
      </template>
    </v-dialog>

    <!-- Form -->
    <v-dialog v-model="data.dialog4" max-width="500">
      <template v-slot:default="{ isActive }">
        <v-card rounded="lg">
          <v-card-title class="d-flex justify-space-between align-center">
            <div class="text-h5 text-medium-emphasis ps-2">Invite John to connect</div>
            <v-btn icon="mdi-close" variant="text" @click="isActive.value = false"></v-btn>
          </v-card-title>
          <v-divider class="mb-4"></v-divider>
          <v-card-text>
            <div class="text-medium-emphasis mb-4">Invite collaborators to your network and grow your connections.</div>
            <div class="mb-2">Message (optional)</div>
            <v-textarea :counter="300" class="mb-2" rows="2" variant="outlined" persistent-counter></v-textarea>
            <div class="text-overline mb-2">💎 PREMIUM</div>
            <div class="text-medium-emphasis mb-1">
              Share with unlimited people and get more insights about your network. Try Premium Free for 30 days.
            </div>
            <v-btn class="text-none font-weight-bold ms-n4" color="primary" text="Retry Premium Free" variant="text"></v-btn>
          </v-card-text>
          <v-divider class="mt-2"></v-divider>
          <v-card-actions class="my-2 d-flex justify-end">
            <v-btn class="text-none" rounded="xl" text="Cancel" @click="isActive.value = false"></v-btn>
            <v-btn class="text-none" rounded="xl" text="Send" color="primary" @click="isActive.value = false"></v-btn>
          </v-card-actions>
        </v-card>
      </template>
    </v-dialog>
  </template>
</template>

<script setup lang="ts">
import UiParentCard from '@/components/shared/UiParentCard.vue';
import UiChildCard from '@/components/shared/UiChildCard.vue';

const data = reactive({
  dialog1: false,
  dialog2: false,
  dialog3: false,
  dialog4: false,
  dialog5: false,
  dialog6: false,
  dialog7: false,
  dialog8: false,
  dialog9: false
});

const page = {
  init() {},
  btnAlert1() {
    max.ui.alert('Alert 메세지 내용입니다.');
  },
  btnAlert2() {
    max.ui.alert({
      title: 'Alert 타이틀',
      content: 'Alert 메세지 내용입니다.',
      buttons: {
        ok: {
          text: '확인',
          action: function () {
            console.log('alert.ok');
          }
        }
      }
    });
  },
  btnConfirm() {
    max.ui.confirm({
      title: 'Confirm 타이틀',
      content: 'Confirm 메세지 내용입니다.',
      buttons: {
        ok: {
          text: '확인',
          action() {
            console.log('confirm.ok');
          }
        },
        cancel: {
          text: '취소',
          action() {
            console.log('confirm.cancel');
          }
        }
      }
    });
  },
  btnValid() {
    max.ui.valid('Valid 메세지 내용입니다.');
  },
  btnError() {
    max.ui.error({
      title: '오류',
      content: 'Error 메세지 내용입니다.'
    });
  }
};
</script>
