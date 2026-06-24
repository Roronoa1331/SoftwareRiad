import {
  buildTriplePreview,
  CulturalRelic,
  getOfflineRelics,
  getOfflineStats,
  KgStats,
  KgTriplePreview
} from '../models/Artifact';
import { KnowledgeGraphApi } from '../services/KnowledgeGraphApi';

@Entry
@Component
struct Index {
  @State relics: CulturalRelic[] = getOfflineRelics();
  @State stats: KgStats = getOfflineStats(getOfflineRelics());
  @State searchQuery: string = '';
  @State selectedRelic: CulturalRelic | null = null;
  @State isLoading: boolean = false;
  @State dataSource: string = 'Offline sample · The Met Museum (New York)';

  aboutToAppear(): void {
    this.applyOfflineData();
    this.tryLiveRefresh();
  }

  applyOfflineData(): void {
    this.relics = KnowledgeGraphApi.getOfflineArtifacts(this.searchQuery);
    this.stats = KnowledgeGraphApi.getOfflineKgStats();
    this.dataSource = 'Offline sample · The Met Museum (New York)';
    this.isLoading = false;
  }

  async tryLiveRefresh(): Promise<void> {
    const live = await KnowledgeGraphApi.tryFetchLive(this.searchQuery);
    if (live !== null) {
      this.relics = live.relics;
      this.stats = live.stats;
      this.dataSource = 'Live data · MySQL + Neo4j dual storage';
    }
  }

  onSearchSubmit(): void {
    this.isLoading = true;
    this.relics = KnowledgeGraphApi.getOfflineArtifacts(this.searchQuery);
    this.stats = getOfflineStats(this.relics.length > 0 ? this.relics : getOfflineRelics());
    this.isLoading = false;
    this.tryLiveRefresh();
  }

  build() {
    Column() {
      this.HeaderSection()
      this.StatsSection()
      this.SearchSection()
      this.ContentSection()
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#F5F0E8')
  }

  @Builder
  ContentSection() {
    if (this.isLoading) {
      Column() {
        LoadingProgress()
          .width(48)
          .height(48)
          .color('#8B4513')
        Text('Loading...')
          .fontSize(13)
          .fontColor('#888888')
          .margin({ top: 12 })
      }
      .width('100%')
      .layoutWeight(1)
      .justifyContent(FlexAlign.Center)
    } else if (this.selectedRelic !== null) {
      this.DetailSection()
    } else if (this.relics.length === 0) {
      Column() {
        Text('No artifacts found')
          .fontSize(16)
          .fontColor('#666666')
        Text('Try a different search term')
          .fontSize(13)
          .fontColor('#999999')
          .margin({ top: 8 })
      }
      .width('100%')
      .layoutWeight(1)
      .justifyContent(FlexAlign.Center)
    } else {
      this.RelicListSection()
    }
  }

  @Builder
  HeaderSection() {
    Column() {
      Text('Chinese Cultural Relics')
        .fontSize(26)
        .fontWeight(FontWeight.Bold)
        .fontColor('#2C1810')
      Text('Knowledge Graph Subsystem · 6.3.1')
        .fontSize(14)
        .fontColor('#8B6914')
        .margin({ top: 4 })
      Text('Overseas Museum Collection · The Metropolitan Museum of Art')
        .fontSize(12)
        .fontColor('#666666')
        .margin({ top: 2 })
    }
    .width('100%')
    .padding({ top: 48, bottom: 16, left: 20, right: 20 })
    .alignItems(HorizontalAlign.Start)
    .backgroundColor('#E8DCC8')
  }

  @Builder
  StatsSection() {
    Row() {
      this.StatCard('Artifacts', `${this.stats.mysql_artifacts}`, '#8B4513')
      this.StatCard('Graph Nodes', `${this.stats.neo4j_nodes}`, '#2E5984')
      this.StatCard('Relations', `${this.stats.neo4j_relationships}`, '#4A6741')
    }
    .width('100%')
    .padding({ left: 16, right: 16, bottom: 12 })
    .justifyContent(FlexAlign.SpaceBetween)
  }

  @Builder
  StatCard(label: string, value: string, color: string) {
    Column() {
      Text(value)
        .fontSize(22)
        .fontWeight(FontWeight.Bold)
        .fontColor(color)
      Text(label)
        .fontSize(11)
        .fontColor('#666666')
        .margin({ top: 4 })
    }
    .width('30%')
    .padding(12)
    .backgroundColor('#FFFFFF')
    .borderRadius(12)
    .shadow({ radius: 6, color: '#1A000000', offsetY: 2 })
  }

  @Builder
  SearchSection() {
    Row() {
      TextInput({ placeholder: 'Search by name, dynasty, material...', text: this.searchQuery })
        .layoutWeight(1)
        .height(40)
        .backgroundColor('#FFFFFF')
        .borderRadius(20)
        .padding({ left: 16, right: 16 })
        .onChange((value: string) => {
          this.searchQuery = value;
        })
        .onSubmit(() => {
          this.onSearchSubmit();
        })
      Button('Search')
        .height(40)
        .margin({ left: 8 })
        .backgroundColor('#8B4513')
        .fontColor('#FFFFFF')
        .borderRadius(20)
        .onClick(() => {
          this.onSearchSubmit();
        })
    }
    .width('100%')
    .padding({ left: 16, right: 16, bottom: 8 })
  }

  @Builder
  RelicListSection() {
    Scroll() {
      Column({ space: 12 }) {
        Text(`${this.dataSource} · ${this.relics.length} items`)
          .fontSize(11)
          .fontColor('#999999')
          .width('100%')
          .textAlign(TextAlign.Center)
          .margin({ bottom: 4 })

        ForEach(this.relics, (relic: CulturalRelic) => {
          Column() {
            this.RelicCard(relic)
          }
          .onClick(() => {
            this.selectedRelic = relic;
          })
        }, (relic: CulturalRelic) => relic.artifact_id)
      }
      .width('100%')
      .padding({ left: 16, right: 16, bottom: 24 })
    }
    .layoutWeight(1)
    .width('100%')
    .scrollBar(BarState.Auto)
    .edgeEffect(EdgeEffect.Spring)
  }

  @Builder
  RelicCard(relic: CulturalRelic) {
    Row() {
      Image(relic.image_url)
        .width(88)
        .height(88)
        .borderRadius(8)
        .objectFit(ImageFit.Cover)
        .backgroundColor('#E0E0E0')
        .alt(relic.name)

      Column() {
        Text(relic.name)
          .fontSize(16)
          .fontWeight(FontWeight.Medium)
          .fontColor('#2C1810')
          .maxLines(2)
          .textOverflow({ overflow: TextOverflow.Ellipsis })

        if (relic.dynasty !== undefined && relic.dynasty.length > 0) {
          Text(relic.dynasty)
            .fontSize(12)
            .fontColor('#8B6914')
            .margin({ top: 4 })
        }

        if (relic.material !== undefined && relic.material.length > 0) {
          Text(relic.material)
            .fontSize(11)
            .fontColor('#666666')
            .maxLines(1)
            .textOverflow({ overflow: TextOverflow.Ellipsis })
            .margin({ top: 2 })
        }

        Text(relic.museum_name)
          .fontSize(10)
          .fontColor('#999999')
          .margin({ top: 4 })
      }
      .alignItems(HorizontalAlign.Start)
      .layoutWeight(1)
      .margin({ left: 12 })
    }
    .width('100%')
    .padding(12)
    .backgroundColor('#FFFFFF')
    .borderRadius(12)
    .shadow({ radius: 4, color: '#15000000', offsetY: 2 })
  }

  @Builder
  DetailSection() {
    Scroll() {
      Column() {
        Button('← Back to list')
          .backgroundColor(Color.Transparent)
          .fontColor('#8B4513')
          .alignSelf(ItemAlign.Start)
          .onClick(() => {
            this.selectedRelic = null;
          })

        if (this.selectedRelic !== null) {
          Image(this.selectedRelic.image_url)
            .width('100%')
            .height(260)
            .borderRadius(12)
            .objectFit(ImageFit.Cover)
            .backgroundColor('#E0E0E0')
            .margin({ top: 8 })
            .alt(this.selectedRelic.name)

          Text(this.selectedRelic.name)
            .fontSize(22)
            .fontWeight(FontWeight.Bold)
            .fontColor('#2C1810')
            .margin({ top: 16 })

          this.DetailRow('Dynasty', this.selectedRelic.dynasty ?? '—')
          this.DetailRow('Age', this.selectedRelic.age ?? '—')
          this.DetailRow('Type', this.selectedRelic.artifact_type ?? '—')
          this.DetailRow('Material', this.selectedRelic.material ?? '—')
          this.DetailRow('Artist', this.selectedRelic.artist ?? '—')
          this.DetailRow('Museum', this.selectedRelic.museum_name)
          this.DetailRow('Location', this.selectedRelic.museum_location ?? '—')

          Text('Introduction')
            .fontSize(14)
            .fontWeight(FontWeight.Bold)
            .fontColor('#8B6914')
            .margin({ top: 16, bottom: 8 })
            .alignSelf(ItemAlign.Start)

          Text(this.selectedRelic.introduction ?? '')
            .fontSize(14)
            .fontColor('#444444')
            .lineHeight(22)

          Text(`Knowledge Graph Relations (${buildTriplePreview(this.selectedRelic).length})`)
            .fontSize(14)
            .fontWeight(FontWeight.Bold)
            .fontColor('#2E5984')
            .margin({ top: 20, bottom: 8 })
            .alignSelf(ItemAlign.Start)

          ForEach(buildTriplePreview(this.selectedRelic), (triple: KgTriplePreview) => {
            this.TripleRow(triple.predicate, triple.object)
          }, (triple: KgTriplePreview) => `${triple.predicate}_${triple.object}`)
        }
      }
      .width('100%')
      .padding(16)
    }
    .layoutWeight(1)
    .width('100%')
  }

  @Builder
  DetailRow(label: string, value: string) {
    Row() {
      Text(label)
        .fontSize(13)
        .fontColor('#888888')
        .width('28%')
      Text(value)
        .fontSize(13)
        .fontColor('#2C1810')
        .layoutWeight(1)
    }
    .width('100%')
    .margin({ top: 8 })
  }

  @Builder
  TripleRow(predicate: string, objectValue: string) {
    Row() {
      Text(this.selectedRelic?.name ?? 'Artifact')
        .fontSize(12)
        .fontColor('#8B4513')
        .maxLines(1)
        .textOverflow({ overflow: TextOverflow.Ellipsis })
        .layoutWeight(1)
      Text(predicate)
        .fontSize(11)
        .fontColor('#2E5984')
        .margin({ left: 4, right: 4 })
      Text(objectValue)
        .fontSize(12)
        .fontColor('#4A6741')
        .maxLines(2)
        .textOverflow({ overflow: TextOverflow.Ellipsis })
        .layoutWeight(1)
    }
    .width('100%')
    .padding(8)
    .margin({ bottom: 6 })
    .backgroundColor('#FFFFFF')
    .borderRadius(8)
  }
}
