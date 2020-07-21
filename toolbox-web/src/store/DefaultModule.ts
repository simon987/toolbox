import {VuexModule, Module, Mutation, Action} from 'vuex-module-decorators'

@Module({namespaced: true, name: 'def'})
class DefaultModule extends VuexModule {
  public status = '>'

  @Mutation
  public setStatus(newStatus: string): void {
    this.status = newStatus
  }
}

export default DefaultModule
