<template>
  <div>
    <q-splitter
      v-model="splitterModel"
      style="height: 400px"
    >

      <template v-slot:before>
        <div class="q-pa-md">
          <q-tree
            :nodes="simple"
            node-key="label"
            selected-color="primary"
            :selected.sync="selected"
            default-expand-all
          />
        </div>
      </template>

      <template v-slot:after>
        <q-tab-panels
          v-model="selected"
          animated
          transition-prev="jump-up"
          transition-next="jump-up"
        >
          <q-tab-panel name="Doctor List">
            <div class="text-h4 q-mb-md">Welcome</div>
            <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quis praesentium cumque magnam odio iure quidem, quod illum numquam possimus obcaecati commodi minima assumenda consectetur culpa fuga nulla ullam. In, libero.</p>
            <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quis praesentium cumque magnam odio iure quidem, quod illum numquam possimus obcaecati commodi minima assumenda consectetur culpa fuga nulla ullam. In, libero.</p>
          </q-tab-panel>

          <q-tab-panel name="Dr.Mark Jacob">
            <div class="text-h4 q-mb-md">Dr.Mark Jacob</div>
            <p>
              Dr.	Mark Jacob	was	born	in	DuBois,	Pennsylvania	and	is	a	graduate	of	Villanova
              University.	He	obtained	his	medical	degree	at	Thomas	Jefferson	University	in
              Philadelphia.	His	residency	was	at	Thomas	Jefferson	and	its	affiliated	Wills	Eye
              Hospital,	and	he	completed	his	training	with	fellowships	at	the	University	of
              Connecticut in	cataract	and	corneal	surgery.
            </p>
            <p>
              Dr.	Jacob	has	thirty	years’	experience	in	ophthalmic	surgery,	with	special	interest	in
              cataract	surgery,	corneal	transplantation,	and	laser	refractive	procedures.	He	is	a
              founding	member	of	Precision	LASIK	Group,	Chief	of	Ophthalmology	at	The	Hospital
              of	Central	Connecticut,	and	co-medical	director	of	the	Connecticut	eye	bank.
              In	addition	to	his	surgical	practice,	he	is	on	the	board	of	Vision	Health	International,
              an	organization	providing	eye	care	and	surgery	to	indigent	patients	in	Central	and
              South	America.
            </p>

            <q-btn color="red" icon="assignment_turned_in" icon-right="send" label="Send Permissions" />

          </q-tab-panel>

          <q-tab-panel name="Dr.John Doe">
            <div class="text-h4 q-mb-md">Dr.John Doe</div>
            <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quis praesentium cumque magnam odio iure quidem, quod illum numquam possimus obcaecati commodi minima assumenda consectetur culpa fuga nulla ullam. In, libero.</p>
            <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quis praesentium cumque magnam odio iure quidem, quod illum numquam possimus obcaecati commodi minima assumenda consectetur culpa fuga nulla ullam. In, libero.</p>
            <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quis praesentium cumque magnam odio iure quidem, quod illum numquam possimus obcaecati commodi minima assumenda consectetur culpa fuga nulla ullam. In, libero.</p>

            <q-btn color="red" icon="assignment_turned_in" icon-right="send" label="Send Permissions" />
          </q-tab-panel>

          <q-tab-panel name="Dr.Ana Markovie">
            <div class="text-h4 q-mb-md">Dr.Ana Markovie</div>
            <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quis praesentium cumque magnam odio iure quidem, quod illum numquam possimus obcaecati commodi minima assumenda consectetur culpa fuga nulla ullam. In, libero.</p>
            <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quis praesentium cumque magnam odio iure quidem, quod illum numquam possimus obcaecati commodi minima assumenda consectetur culpa fuga nulla ullam. In, libero.</p>
            <q-btn color="red" icon="assignment_turned_in" icon-right="send" label="Send Permissions" />
          </q-tab-panel>

        </q-tab-panels>
      </template>
    </q-splitter>
  </div>
</template>

<script>
export default {
  data () {
    return {
      splitterModel: 50,
      selected: '',
      simple: [
        {
          label: 'Doctor List',
          children: [
            {
              label: 'Dr.Mark Jacob',
              icon: 'assignment_ind'
            },
            {
              label: 'Dr.John Doe',
              icon: 'assignment_ind'
            },
            {
              label: 'Dr.Ana Markovie',
              icon: 'assignment_ind'
            }
          ]
        }
      ]
    }
  }
}
</script>
